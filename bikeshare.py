import time
import pandas as pd
import numpy as np

CITY_DATA = { 'C': 'chicago.csv',
              'NYC': 'new_york_city.csv',
              'W': 'washington.csv' }

name = str(input('Before we get started, please enter your first name here:'))
print('Hello {}! Let\'s explore some US bikeshare data!'.format(name.title()))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('\n About which city do you want to learn more about? Please enter \n C for Chicago, \n NYC for New York City or \n W for Washington.\n Enter your answer here:'))
        except:
            print('\n That is not a valid answer! Please type in the correct option as stated above.\n')
        else:
            if city not in ('C', 'NYC', 'W'):
                print('It looks like you made a spelling mistake - please provide the right abbrevation, which is either C, NYC or W.')
            else:
                break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('\n Okay, now please select the month you want to look into. Please choose between January, February, March, April, May or June. \n You can also go for all months by selecting all.'))
        except:
            print('\n That is not a valid answer! Please type in the correct option as stated above.\n')
        else:
            if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'all'):
                print('It looks like you made a spelling mistake - please provide the right month or select "all"')
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('\n Okay, now please select the day you want to look into. Please choose between \n Monday, \n Tuesday,\n Wednesday,\n Thursday, \n Friday, \n Saturday or \n Sunday. \n You can also go for the complete week by selecting all.'))
        except:
            print('\n That is not a valid answer! Please type in the correct option as stated above.\n')
        else:
            if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday', 'all'):
                print('It looks like you made a spelling mistake - please provide the right day or select "all"')
            else:
                break

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def raw_data(df):
    while True:
        try:
            raw_data = str(input('Would you like to see some individual data first?Please type in either yes or no.'))
        except ValueError:
            print('\n That is not a valid answer! Please type in the correct option as stated above.\n')
        else:
            if raw_data not in ('yes', 'no'):
                print('It looks like you made a spelling mistake - please type in "yes" or "no"')
            else:
                if raw_data == 'yes':
                    print(df.head(5))
                else:
                    break

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]
    print('The most common month (in numbers) was:', pop_month)

    # display the most common day of week
    pop_day = df['day_of_week'].mode()[0]
    print('The most common day of week was:', pop_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    print('The most common start hour was:', pop_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    count_start_station = df['Start Station'].value_counts().head(1)
    print('Show the most commonly used start station and number of times used:', count_start_station)

    # display most commonly used end station
    count_end_station = df['End Station'].value_counts().head(1)
    print('Show the most commonly used end station and number of times used:', count_end_station)

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' - ' + df['End Station']
    pop_station_combination = df['Station Combination'].value_counts().head(1)
    print('Show the most commonly used station combination and number of times used:', pop_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('This is the total trip duration in seconds:', total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('This is the mean travel time in seconds:', mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('These are the different counts per user type:\n', user_types)

    # Display counts of gender
    if 'Gender' not in df:
        print('There is no gender information available')
    else:
        gender = df['Gender'].value_counts()
        print('These are the different counts per gender:\n', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('There is no birth year information available')
    else:
        min_year = df['Birth Year'].min()
        print('This is the earliest birth year of users:', int(min_year))
        max_year = df['Birth Year'].max()
        print('This is the most recent birth year of users:', int(max_year))
        mean_year = df['Birth Year'].mean()
        print('This is the mean birth year of users:', int(mean_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data (df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
