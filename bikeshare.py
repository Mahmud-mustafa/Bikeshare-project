import time
import numpy as np
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities=['chicago','new york city','washington']
months=['january','february','march','april','may','june']
days=['saturday','sunday','monday','tuesday','wednesday','thursday','friday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city=input('Please enter city to analyze:Chicago ,New york city or Washington (enter exact name)\n').lower()
        if city not in cities:
            print('check input : city not in cities list')
            continue
        break
    while True:
        filter_choice=input('Do you want to filter with days ,months ,both or none?\n').lower()
        filters=['days','months','both','none']
        if filter_choice not in filters:
            print("invalid input: enter 'months' ,'days' , 'both' or 'none'")
            continue
        break
    while True:
        if str(filter_choice) == 'both':
            month=input("Please enter the month to filter with (range:[1:6]).\n").lower()
            day=input("Please enter the day to filter with. \n").lower()
            if month not in months or day not in days:
                print('check input : month not in range or day invalid')
                continue
            break
        elif str(filter_choice)== 'months':
            month=input("Please enter the month to filter with (range:[1:6]).\n").lower()
            day='all'
            if month not in months:
                print('check input : month not in range ')
                continue
            break
        elif str(filter_choice)=='days':
            month='all'
            day=input("Please enter the day to filter with.\n").lower()
            if day not in days:
                print('check input : day invalid')
                continue
            break
        elif str(filter_choice)=='none':
            month='all'
            day='all'
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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['Month']=df['Start Time'].dt.month
    df['Day']=df['Start Time'].dt.day_name
    if month !='all':
        month=months.index(month)+1
        df=df[df['Month']==month]
    if day !='all':
        day=day.title()
        df=df[df['Day']==day]
    df.fillna(method='ffill',axis=0,inplace=True)
    #couldn't find any other why to clean NaN values tbh.
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Hour']=df['Start Time'].dt.hour
    print('The most common month : {}.'.format( months[ df['Month'].mode()[0] - 1] ) )
    print('The most common weekday : {}.'.format( df['Day'].mode()[0] ) )
    common_hour=int(df['Hour'].mode()[0])
    if common_hour - 12 < 0:
        print('The most common hour : {} am.'.format(abs(common_hour - 12)))
    elif common_hour - 12 > 0:
        print('The most common hour : {} pm.'.format(common_hour))
    df.pop('Day')
    df.pop('Month')
    df.pop('Hour')
    #bet no one did it this way.
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['Trip']='From ' + df['Start Station'] + ' to ' + df['End Station']
    print('The most commonly used start station : {}.'.format( df['Start Station'].mode()[0] ) )
    
    print('The most commonly used end station : {}.'.format( df['End Station'].mode()[0] ) )

    print('The most frequent combination of start station and end station trip : {}.'.format( df['Trip'].mode()[0] ) ) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    df.pop('Trip')
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    sum_time=df['Trip Duration'].sum()
    avg_time=df['Trip Duration'].mean()
    pd.set_option('precision',1)
    print('Total travel time : {} seconds , {} minutes , {} hours.'.format(sum_time,sum_time / 60,sum_time / 3600) )
    
    print('Average travel time : {} seconds , {} minutes , {} hours.'.format(avg_time,avg_time / 60,avg_time / 3600)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('Printing user type stats :-\n')
    print(df['User Type'].value_counts().to_string()) 
    # TO DO: Display counts of gender
    try:
        print('Printing user gender stats:-\n') 
        print(df['Gender'].value_counts().to_string())
    except KeyError:
        print("There's no gender data available.")
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('Printing user birth year stats:-\n')
        print('Earliest birth year : {}.'.format(df['Birth Year'].min() ) ) 
        print('Most recent birth year : {}.'.format(df['Birth Year'].max() ) ) 
        print('Most common birth year: {}.'.format(df['Birth Year'].mode()[0] ) )
    except KeyError:
        print("There's no birth year data available") 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_file(df):
    choice=input('would you like to display raw data?(yes/no)\n')
    if choice.lower() == 'yes':
        num_rows=int(input('enter how many rows you want displayed.\n'))
        start=0
        end=num_rows
        while True:
            if num_rows <= len(df):
                print(df[start:end])
            else:
                print('exceeded number of rows of file.')
            start+=num_rows
            end+=num_rows
            again=input('display again?(yes/no)')
            if again.lower()!= 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_file(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
