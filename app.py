"""IPL 2026 Stadium Intelligence — APD project. All occupancy figures are scenarios."""
from pathlib import Path
import base64
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import binom, beta as beta_dist, poisson

BASE = Path(__file__).resolve().parent
st.set_page_config(page_title='IPL 2026 | Stadium Intelligence', page_icon='🏏', layout='wide')


def file_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode('utf-8')


BG_B64 = file_to_base64(BASE / 'ipl_background.webp') if (BASE / 'ipl_background.webp').exists() else ''

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{font-family:'Inter',sans-serif;}}
[data-testid="stAppViewContainer"] {{
    background:
        linear-gradient(rgba(2,8,23,0.88), rgba(2,8,23,0.93)),
        url("data:image/webp;base64,{BG_B64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{background: rgba(2,8,23,0.15);}}
.block-container {{padding-top:1.15rem; max-width:1500px;}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(4,12,30,0.98) 0%, rgba(9,26,58,0.98) 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}}
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarNav"] {{background: transparent;}}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] div {{color: #e6eefc;}}
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stDateInput,
section[data-testid="stSidebar"] .stRadio,
section[data-testid="stSidebar"] .stSelectbox {{
    background: rgba(255,255,255,0.035);
    border-radius: 16px;
    padding: 0.15rem 0.15rem 0.35rem 0.15rem;
    border: 1px solid rgba(255,255,255,0.06);
}}

.hero-wrap {{
    background: linear-gradient(135deg, rgba(16,30,67,0.86), rgba(4,13,31,0.78));
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 14px 30px rgba(0,0,0,0.25);
    border-radius: 24px;
    padding: 26px 28px 20px 28px;
    margin-bottom: 14px;
    backdrop-filter: blur(10px);
}}
.hero-title {{font-size: 2.35rem; font-weight: 800; color: #ffffff; letter-spacing: -0.03em; margin-bottom: 0.25rem;}}
.hero-subtitle {{font-size: 1rem; color: #d4ddf3; margin-bottom: 0.7rem;}}
.hero-chip {{display:inline-block; padding:7px 12px; margin:4px 7px 0 0; border-radius:999px; background:rgba(255,255,255,0.08); color:#eff6ff; font-size:0.88rem; border:1px solid rgba(255,255,255,0.08);}}
.notice-box {{
    background: linear-gradient(90deg, rgba(120,113,8,0.45), rgba(133,77,14,0.42));
    color:#fff7d6; border:1px solid rgba(251,191,36,0.25); border-radius:18px; padding:16px 18px; margin: 12px 0 18px 0;
}}
.panel-card {{
    background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}}
.panel-title {{font-size: 1.1rem; font-weight: 700; color:#fff; margin-bottom:0.35rem;}}
.panel-text {{font-size: 0.95rem; color:#dbe7ff;}}

h1,h2,h3 {{color:#f8fafc !important;}}
.stCaption, small {{color:#c8d4ec !important;}}
[data-testid="stMetric"] {{
    background: linear-gradient(180deg, rgba(255,255,255,0.11), rgba(255,255,255,0.06));
    border:1px solid rgba(255,255,255,0.08);
    border-radius:20px; padding:16px 18px; box-shadow:0 10px 24px rgba(0,0,0,0.18);
}}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{color:#f8fafc !important;}}
[data-testid="stMetricDelta"] {{color:#dbeafe !important;}}

.stTabs [data-baseweb="tab-list"] {{gap:10px;}}
.stTabs [data-baseweb="tab"] {{
    height:50px; background: rgba(255,255,255,0.05); border-radius: 14px 14px 0 0; padding: 0 16px;
    color:#d6e1f7; font-weight:700; border:1px solid rgba(255,255,255,0.05);
}}
.stTabs [aria-selected="true"] {{background: linear-gradient(180deg, rgba(37,99,235,0.26), rgba(168,85,247,0.16)) !important; color: #ffffff !important;}}

.stButton > button, .stDownloadButton > button {{
    border-radius: 14px; border: none; background: linear-gradient(90deg, #2563eb, #7c3aed); color:white; font-weight:700;
    box-shadow: 0 10px 18px rgba(37,99,235,0.25);
}}

.stDataFrame, div[data-testid="stTable"] {{
    background: rgba(8,15,31,0.62); border:1px solid rgba(255,255,255,0.08); border-radius:18px; padding:8px;
}}

div[data-testid="stExpander"] {{background: rgba(255,255,255,0.04); border-radius:16px;}}
.element-container img {{border-radius: 18px; box-shadow: 0 10px 28px rgba(0,0,0,0.22);}}
hr {{border-color: rgba(255,255,255,0.08);}}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_files():
    m = pd.read_excel(BASE / 'IPL 2026.xlsx', sheet_name='All 74 Matches')
    s = pd.read_excel(BASE / 'IPL 2026.xlsx', sheet_name='Stadium Capacities')
    prices = pd.read_csv(BASE / 'stadium_ticket_prices.csv', encoding='utf-8-sig')
    images = pd.read_csv(BASE / 'image_manifest.csv', encoding='utf-8-sig').fillna('')
    m['Date'] = pd.to_datetime(m['Date'], errors='coerce')
    for name in ['Stadium capacity', 'Actual attendance', 'Estimated attendance', 'Low scenario crowd',
                 'High scenario crowd', 'Model occupancy assumption']:
        m[name] = pd.to_numeric(m[name], errors='coerce')
    m['Estimated occupancy %'] = (100 * m['Estimated attendance'] / m['Stadium capacity']).clip(0, 100)
    m['Fixture'] = m['Team 1'].astype(str) + ' vs ' + m['Team 2'].astype(str)
    m['Match day'] = np.where(m['Date'].dt.weekday >= 5, 'Weekend', 'Weekday')
    prices['Indicative ticket price (INR)'] = pd.to_numeric(prices['Indicative ticket price (INR)'], errors='coerce')
    return m, s, prices, dict(zip(images['Exact stadium name in workbook'], images['Image path']))


matches, stadiums, prices, image_paths = load_files()
venues = sorted(matches['Stadium'].dropna().unique())

st.markdown(
    """
<div class="hero-wrap">
    <div class="hero-title">🏏 IPL 2026 · Stadium Intelligence</div>
    <div class="hero-subtitle">Match analytics · stadium seating maps · ticket pricing · applied probability · revenue simulation</div>
    <span class="hero-chip">74 matches</span>
    <span class="hero-chip">13 venues</span>
    <span class="hero-chip">13 seating-map images integrated</span>
    <span class="hero-chip">APD project dashboard</span>
</div>
<div class="notice-box"><b>Data classification:</b> Attendance and occupancy are <b>modelled estimates</b>, not verified match-day crowds. Prices are <b>indicative values from supplied illustrative maps</b>, not a match-complete ticket sales dataset. Revenue figures are <b>hypothetical scenarios</b>.</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('### 🎛️ Dashboard filters')
    selected_venues = st.multiselect('Stadium', venues, default=venues)
    teams = sorted(set(matches['Team 1'].dropna()) | set(matches['Team 2'].dropna()))
    selected_teams = st.multiselect('Teams (either side)', teams)
    stages = sorted(matches['Stage'].dropna().unique())
    selected_stages = st.multiselect('Match stage', stages, default=stages)
    day = st.radio('Match day', ['All', 'Weekend', 'Weekday'], horizontal=True)
    valid_dates = matches['Date'].dropna()
    if not valid_dates.empty:
        range_dates = st.date_input('Date range', value=(valid_dates.min().date(), valid_dates.max().date()))
    else:
        range_dates = ()
    st.caption('These filters change the Overview and match-level tables. Statistical simulations use their own controls.')

view = matches[matches['Stadium'].isin(selected_venues) & matches['Stage'].isin(selected_stages)].copy()
if selected_teams:
    view = view[view['Team 1'].isin(selected_teams) | view['Team 2'].isin(selected_teams)]
if day != 'All':
    view = view[view['Match day'] == day]
if len(range_dates) == 2:
    view = view[view['Date'].dt.date.between(*range_dates)]

st_tabs = st.tabs(['📊 Overview', '🏟️ Stadium Explorer', '🎟️ Ticket Pricing', '🧪 Probability Lab', '💰 Revenue Simulator', '📁 Data & Methods'])

with st_tabs[0]:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric('Matches', f'{len(view):,}')
    k2.metric('Stadiums', f'{view["Stadium"].nunique():,}')
    k3.metric('Total estimated spectators', f'{view["Estimated attendance"].sum():,.0f}')
    k4.metric('Average estimated occupancy', f'{view["Estimated occupancy %"].mean():.1f}%' if not view.empty else '—')
    if view.empty:
        st.info('No matches match the current filters. Change the sidebar filters.')
    else:
        summary = (view.groupby('Stadium', as_index=False).agg(
            Matches=('Match No', 'count'), Capacity=('Stadium capacity', 'max'),
            Average_occupancy=('Estimated occupancy %', 'mean'),
            Average_attendance=('Estimated attendance', 'mean')))
        a, b = st.columns(2)
        with a:
            fig = px.bar(summary.sort_values('Average_occupancy'), x='Average_occupancy', y='Stadium', orientation='h',
                         color='Average_occupancy', color_continuous_scale='Blues', labels={'Average_occupancy': 'Estimated occupancy (%)'},
                         title='Average scenario occupancy by venue')
            fig.update_layout(height=510, coloraxis_showscale=False, margin=dict(l=5, r=5),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                              font_color='#f8fafc')
            st.plotly_chart(fig, use_container_width=True)
        with b:
            fig = px.scatter(view, x='Stadium capacity', y='Estimated attendance', color='City',
                             hover_data=['Fixture', 'Date', 'Estimated occupancy %'],
                             title='Nominal capacity vs modelled attendance')
            maxc = view['Stadium capacity'].max()
            fig.add_trace(go.Scatter(x=[0, maxc], y=[0, maxc], mode='lines',
                                     line=dict(dash='dash', color='gray'), name='100% occupancy'))
            fig.update_layout(height=510, margin=dict(l=5, r=5),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                              font_color='#f8fafc')
            st.plotly_chart(fig, use_container_width=True)
        st.subheader('Matches in the selected dataset')
        st.dataframe(view[['Match No', 'Date', 'Fixture', 'Stage', 'Start time', 'Stadium', 'Stadium capacity',
                           'Estimated attendance', 'Estimated occupancy %']].sort_values('Match No'),
                     hide_index=True, use_container_width=True)

with st_tabs[1]:
    st.subheader('Explore stadiums and stand-wise seating diagrams')
    venue = st.selectbox('Choose stadium', venues, key='explore_venue')
    subset = matches[matches['Stadium'] == venue].copy()
    cap = int(subset['Stadium capacity'].dropna().iloc[0])
    psub = prices[prices['Stadium'] == venue].copy()
    a, b, c, d = st.columns(4)
    a.metric('Nominal capacity', f'{cap:,}')
    b.metric('Hosted matches', f'{len(subset)}')
    c.metric('Average estimated occupancy', f'{subset["Estimated occupancy %"].mean():.1f}%')
    d.metric('Pricing categories', len(psub))
    colmap, colinfo = st.columns([1.12, 1], gap='large')
    with colmap:
        fp = image_paths.get(venue, '')
        imagefile = BASE / fp if fp else None
        if imagefile and imagefile.is_file():
            st.image(str(imagefile), caption=f'{venue} — user-supplied illustrative seating and pricing infographic', use_container_width=True)
        else:
            st.info('No stadium seating image uploaded for this venue yet. Its attendance figures are still available below.')
    with colinfo:
        st.markdown('#### Stand-wise indicative ticket prices')
        if psub.empty:
            st.info('No stand-wise price categories supplied for this venue.')
        else:
            st.dataframe(psub[['Stand / category', 'Indicative ticket price (INR)', 'Price note']],
                         hide_index=True, use_container_width=True)
            fig = px.bar(psub.sort_values('Indicative ticket price (INR)'), x='Indicative ticket price (INR)',
                         y='Stand / category', orientation='h', title='Indicative price per ticket (₹)',
                         labels={'Indicative ticket price (INR)': 'Ticket price (₹)'})
            fig.update_layout(height=max(350, 35 * len(psub) + 110), margin=dict(l=0, r=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
                              font_color='#f8fafc')
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('#### Estimated crowd scenarios by match')
        st.dataframe(subset[['Match No', 'Date', 'Fixture', 'Start time', 'Estimated attendance', 'Low scenario crowd',
                             'High scenario crowd']], hide_index=True, use_container_width=True)
    st.caption('Illustrations are not official seat-selectors. Infographic prices may refer to a specific match; they are not necessarily applicable to every fixture.')

with st_tabs[2]:
    st.subheader('Ticket pricing comparison')
    st.caption('Prices are manually transcribed from the ten uploaded stadium infographics. For ranged prices, midpoint assumptions are marked in the notes.')
    available = sorted(prices['Stadium'].unique())
    selected = st.multiselect('Compare stadiums', available, default=available[:4], key='price_venues')
    pview = prices[prices['Stadium'].isin(selected)]
    if pview.empty:
        st.info('Choose at least one stadium.')
    else:
        c1, c2 = st.columns(2)
        grouped = pview.groupby('Stadium', as_index=False)['Indicative ticket price (INR)'].agg(['min', 'median', 'max']).reset_index()
        with c1:
            fig = px.bar(grouped, x='Stadium', y='median', title='Median listed category price by stadium',
                         labels={'median': 'Median category price (₹)'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)', font_color='#f8fafc')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.box(pview, x='Stadium', y='Indicative ticket price (INR)', points='all',
                         title='Variation in listed prices across categories')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)', font_color='#f8fafc')
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(pview, hide_index=True, use_container_width=True)
        st.download_button('Download filtered ticket prices CSV', pview.to_csv(index=False).encode('utf-8-sig'),
                           file_name='ipl_2026_ticket_prices.csv', mime='text/csv')
    st.info('Category-price means and medians are not seat-weighted ticket averages. We do not have numbers of seats sold in each category.')

with st_tabs[3]:
    st.subheader('Applied Probability Distributions Lab')
    st.caption('These models demonstrate probability concepts with user-selected assumptions; they are not calibrated to real IPL ticket sales.')
    choice = st.selectbox('Select distribution', ['Binomial: occupied seats', 'Beta: occupancy-rate uncertainty',
                                                  'Poisson: booking enquiries per hour'])
    if choice.startswith('Binomial'):
        lab_venue = st.selectbox('Venue for capacity', venues, key='lab_venue')
        n = int(matches.loc[matches['Stadium'] == lab_venue, 'Stadium capacity'].iloc[0])
        prob = st.slider('Per-seat occupancy probability', 0.05, 0.99, 0.85, 0.01)
        threshold = st.slider('Target occupancy (%)', 30, 99, 90)
        cutoff = int(np.ceil(n * threshold / 100))
        mu = n * prob
        sigma = np.sqrt(n * prob * (1 - prob))
        x = np.arange(max(0, int(mu - 4 * sigma)), min(n, int(mu + 4 * sigma)) + 1)
        st.metric('Expected occupied seats', f'{mu:,.0f}')
        st.metric(f'P(occupancy ≥ {threshold}%)', f'{binom.sf(cutoff - 1, n, prob):.4f}')
        st.caption(f'Variance: {n * prob * (1 - prob):,.2f} seats² · Standard deviation: {sigma:,.2f} seats · Assumes independent, identically occupied seats.')
        fig = px.line(x=x, y=binom.pmf(x, n, prob), labels={'x': 'Occupied seats', 'y': 'Probability'}, title='Binomial PMF (central range)')
    elif choice.startswith('Beta'):
        alpha = st.slider('Alpha', 1.0, 35.0, 9.0, 0.5)
        beta_parameter = st.slider('Beta', 1.0, 35.0, 2.0, 0.5)
        x = np.linspace(.001, .999, 500)
        st.metric('Expected occupancy rate', f'{alpha / (alpha + beta_parameter):.1%}')
        st.caption(f'Variance: {alpha * beta_parameter / ((alpha + beta_parameter) ** 2 * (alpha + beta_parameter + 1)):.5f}')
        fig = px.line(x=x, y=beta_dist.pdf(x, alpha, beta_parameter),
                      labels={'x': 'Occupancy rate (fraction)', 'y': 'Probability density'}, title='Beta probability density')
    else:
        lam = st.slider('Assumed mean enquiries per hour', 1, 500, 80)
        threshold = st.number_input('Target minimum enquiries', min_value=0, value=100)
        st.metric(f'P(enquiries ≥ {threshold})', f'{poisson.sf(threshold - 1, lam):.4f}')
        x = np.arange(0, int(lam + 5 * np.sqrt(lam)) + 1)
        fig = px.bar(x=x, y=poisson.pmf(x, lam), labels={'x': 'Enquiries/hour', 'y': 'Probability'}, title='Poisson PMF')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)', font_color='#f8fafc')
    st.plotly_chart(fig, use_container_width=True)

with st_tabs[4]:
    st.subheader('Ticket Revenue — Monte Carlo Scenario Simulator')
    st.info('With no stand-level seat counts or real sales, this tool simulates potential gross sales, not actual revenue or an evidence-based prediction.')
    sim_venue = st.selectbox('Select venue', venues, key='sim_venue')
    cap = int(matches.loc[matches['Stadium'] == sim_venue, 'Stadium capacity'].iloc[0])
    sp = prices[prices['Stadium'] == sim_venue]
    if not sp.empty:
        st.caption(f'{len(sp)} indicative ticket categories are available for this stadium.')
        price_mode = st.radio('Ticket price assumption', ['Single average ticket price', 'Equal share of seats across listed categories'], horizontal=True)
    else:
        st.warning('No price list for this stadium. Use a user-defined ticket price.')
        price_mode = 'Single average ticket price'
    a, b, c = st.columns(3)
    entered_price = a.number_input('Average paid ticket price (₹)', min_value=100, max_value=100000, value=3000, step=100,
                                   disabled=(price_mode != 'Single average ticket price'))
    runs = b.selectbox('Number of Monte Carlo runs', [1000, 5000, 10000], index=1)
    seed = c.number_input('Simulation seed', min_value=0, max_value=100000, value=42)
    mean_rate = st.slider('Mean seat occupancy assumption', 0.4, 0.99, 0.85, 0.01)
    concentration = st.slider('Occupancy concentration (higher = less uncertainty)', 5, 250, 50, 5)
    if price_mode == 'Single average ticket price':
        effective_price = float(entered_price)
    else:
        effective_price = float(sp['Indicative ticket price (INR)'].mean())
        st.caption(f'Equal-share hypothetical category-weighted price: ₹{effective_price:,.0f}. Actual sales shares are unknown; equal allocation is an assumption.')
    st.metric('Assumed average ticket price in model', f'₹{effective_price:,.0f}')
    if st.button('▶ Run revenue simulation', type='primary'):
        rng = np.random.default_rng(int(seed))
        rates = rng.beta(mean_rate * concentration, (1 - mean_rate) * concentration, int(runs))
        sold = rng.binomial(cap, rates)
        gross = sold * effective_price
        st.session_state['sim_v2'] = {
            'venue': sim_venue, 'price': effective_price, 'rate': mean_rate, 'concentration': concentration,
            'runs': runs, 'seed': seed, 'revenue': gross, 'tickets': sold
        }
    sim = st.session_state.get('sim_v2')
    if sim:
        if any([sim['venue'] != sim_venue, sim['price'] != effective_price, sim['rate'] != mean_rate,
                sim['concentration'] != concentration, sim['runs'] != runs, sim['seed'] != seed]):
            st.warning('These outputs are from the previous simulation. Click Run revenue simulation to recalculate.')
        r = sim['revenue']
        k1, k2, k3, k4 = st.columns(4)
        k1.metric('Mean gross scenario revenue', f'₹{np.mean(r) / 1e7:.2f} Cr')
        k2.metric('5th percentile', f'₹{np.quantile(r, .05) / 1e7:.2f} Cr')
        k3.metric('95th percentile', f'₹{np.quantile(r, .95) / 1e7:.2f} Cr')
        k4.metric('Average simulated tickets', f'{np.mean(sim["tickets"]):,.0f}')
        fig = px.histogram(x=r / 1e7, nbins=45, title='Simulated gross revenue distribution',
                           labels={'x': 'Revenue (₹ crore)', 'y': 'Number of simulated outcomes'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)', font_color='#f8fafc')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption('Choose assumptions above, then run the simulator to see the revenue distribution.')
    st.caption('Gross figures do not account for taxes, booking fees, promotions, complimentary tickets, operational restrictions or a tested demand-price relationship.')

with st_tabs[5]:
    st.subheader('Source data and quality checks')
    a, b, c, d = st.columns(4)
    a.metric('Match rows', len(matches))
    b.metric('Distinct venues', matches['Stadium'].nunique())
    c.metric('Images supplied', sum(bool(fp) for fp in image_paths.values()))
    d.metric('Indicative price categories', len(prices))
    st.write(f'**Verified attendance entries:** {matches["Actual attendance"].notna().sum()} of {len(matches)}')
    st.write(f'**Modelled attendance entries:** {matches["Estimated attendance"].notna().sum()} of {len(matches)}')
    st.markdown('#### Stadium image coverage')
    image_summary = pd.DataFrame([
        {'Stadium': v, 'Image': 'Available' if image_paths.get(v) else 'Not supplied',
         'Price categories': len(prices[prices['Stadium'] == v])} for v in venues
    ])
    st.dataframe(image_summary, hide_index=True, use_container_width=True)
    st.markdown('#### Missing values by match-data column')
    st.dataframe(pd.DataFrame({'Column': matches.columns, 'Missing values': matches.isna().sum().values}),
                 hide_index=True, use_container_width=True)
    st.download_button('Download filtered match data (CSV)', view.to_csv(index=False).encode('utf-8-sig'),
                       file_name='ipl_2026_matches_filtered.csv', mime='text/csv')
    st.markdown('''**Statistical cautions**
    - Actual attendance is absent; the estimates are based on assumed occupancy parameters, so do **not** treat occupancy regressions as measured relationships.
    - Illustrated seating maps are not accurate, official stand-by-stand seat selectors and some reference ticket prices differ by fixture.
    - Average category price is not the same as average ticket price paid; realistic total revenue needs section capacity and sold-ticket counts.
    - Low and high spectator scenarios are assumptions, not formal confidence intervals.
    - Poisson enquiry arrivals and independent Binomial seats are teaching models, not verified operational behaviours.
    ''')
