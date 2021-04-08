# uk-covid
Selected programs relating to COVID-19 data in the UK.

Progam graphs recent data of cases by age, hospital admissions by reigion for the whole pandemic and recently.

Works with Anaconda Spyder - some IDLEs may not work with Pandas and Matplotlib by default.

About the data:
Rolling rates are used in the program.
Information below is copied directly from https://coronavirus.data.gov.uk/details/about-data.

Rates are calculated in order to compare areas or population groups of different sizes. All rates currently presented on this website are crude rates expressed per 100,000 population, ie the count (eg cases or deaths) is divided by the denominator population and then multiplied by 100,000, without any adjustment for other factors.

Populations used are Office for National Statistics 2019 mid-year estimates, except for NHS Regions, for which 2019 estimates are not yet available, so 2018 mid-year estimates are used.

This website primarily presents daily data. Counts of cases, admissions, deaths, etc vary from day to day just through natural random changes, but also tend to vary throughout the week systematically, so that rates are consistently lower at weekends for example.

In order to help to identify trends or patterns in the data over time, 7 day rolling averages can be calculated. These are updated daily, but even out the random variation and the weekly seasonality.

Each day's observation is combined with the previous three days and the following three days, and the mean of all seven days' figures is presented.
