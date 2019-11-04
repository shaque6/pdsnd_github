import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_list = ['sunday', 'monday', 'tuesday','wednesday','thursday','friday','saturday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Would you like to see Data for Chicago, New York City, or Washington?')
    city = input().lower()
    while city not in CITY_DATA.keys():
        print('Incorrect input: Would you like to see Data for Chicago, New York City, or Washington?')
        city = input().lower()

    # get user input for month (all, january, february, ... , june)
    print('What month (January - June) would you like to filter the data by? Type "all" for no month filter.')
    month = input().lower()
    while month not in month_list:
        print('Incorrect input: What month (January - June) would you like to filter the data by? Type "all" for no month filter.')
        month = input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('What day would you like to filter the data by? Type "all" for no day filter.')
    day = input().lower()
    while day not in day_list:
        print('Incorrect input: What day would you like to filter the data by? Type "all" for no month filter.')
        day = input().lower()

    print('Showing data for',city)
    print('Showing data for the month of', month, 'and the day =', day)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # create column of combination of start and end stations
    df['combination'] = df['Start Station'] + '-' + df['End Station']
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # if only month of data then say month being displayed
    if len(np.unique(df['month'])) == 1:
        # print('This data is for the month of', month_list[df['month'][2]-1].capitalize())
        print('This data is for the month of', month_list[df['month'].mode()[0]-1].capitalize())
    else:
    # if all months selected then find most popular month
        print('Most common month for rides is', month_list[df['month'].mode()[0]-1].capitalize())

    # display the most common day of week
    # if only one day of data then say day being displayed
    if len(np.unique(df['day_of_week'])) == 1:
        print('This data is based off  of', df['day_of_week'].mode()[0])
    else:
    # if all days selected then find most popular day
        print('Most common day of the week for rides is', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most common start hour is', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station is:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    mostStart,mostEnd = df['combination'].mode()[0].split('-',1)
    print('\n Most frequent combination of start station and end station:')
    print('\t Start Station:', mostStart)
    print('\t End Station:', mostEnd)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total Travel Time:", round(df['Trip Duration'].sum()/86400,2), 'days')

    # display mean travel time
    print("Average Travel Time:", round(np.average(df['Trip Duration'])/60,2), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_types)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nCounts of gender:')
        print(gender_count)
    except:
        print('No gender information to share')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        most_year = int(df['Birth Year'].mode()[0])
        print('\nRider with earliest birth year:', earliest_year)
        print('Rider with most recent birth year:', recent_year)
        print('Rider with most common birth year:', most_year)
    except:
        print('No birth year information to share')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#option for the user to view 5 lines of raw data at a time
def rawdata(city):
    df = pd.read_csv(CITY_DATA[city])
    n = 3
    view = input('\nWould you like to see the raw data? Enter yes or no.\n')
    if view.lower() == 'yes':
        check = True
        print(df.iloc[0:n])
        n +=3
    else:
        check = False

    while check:
        view = input('\nWould you like to continue seeing the raw data? Enter yes or no.\n')
        if view.lower() == 'yes':
            check = True
            print(df.iloc[n-3:n])
            n +=3
        else:
            check = False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # df = load_data('washington', 'may', 'all')
        # print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
