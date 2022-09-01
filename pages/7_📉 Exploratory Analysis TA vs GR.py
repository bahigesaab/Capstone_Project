import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


from sentiment_analysis import plot_time_series_count, plot_time_series_count_google_reviews
from streamlit_objects import get_tripadvisor_reviews, selection_box, display_info, get_reviewers_nationalities_df, \
    display_world_map, get_googlemaps_reviews, selection_box_two, display_map_lebanon

#*****************************************************************************************************#


st.set_page_config(page_title="Comparative Exploratory Analysis of Reviews of Touristic Sites in Lebanon Trip Advisor vs Google Reviews",
                   page_icon="🌄",
                   layout="wide")


st.title("Comparative Exploratory Analysis of Reviews of Touristic Sites in Lebanon Between Trip Advisor and Google Reviews")


#*****************************************************************************************************#


reviews_1 = get_tripadvisor_reviews("final_trip_advisor_reviews_sa.csv")

reviews_2 = get_googlemaps_reviews("final_google_reviews_sa.csv")


st.markdown("""---""")
#*****************************************************************************************************#


attraction_one_cell, attraction_two_cell = st.columns(2)


with attraction_one_cell:

    attraction_box_one = selection_box(reviews_1, "attraction", "attraction from Trip Advisor", disable_box= False)

    reviews_queried_one = reviews_1.query("attraction==@attraction_box_one")




with attraction_two_cell:

    attraction_box_two = selection_box(reviews_2, "attraction", "attraction from Google Reviews", disable_box= False)

    reviews_queried_two = reviews_2.query("attraction==@attraction_box_two")

st.markdown("""---""")

#*****************************************************************************************************#

attraction_name_one = reviews_queried_one["attraction"].iloc[0] if attraction_box_one[0] != "All" else ""
city_name_one = reviews_queried_one["location"].iloc[0] if attraction_box_one[0] != "All" else ""
governorate_name_one = reviews_queried_one["governorate"].iloc[0] if attraction_box_one[0] != "All" else ""


attraction_name_two = reviews_queried_two["attraction"].iloc[0] if attraction_box_two[0] != "All" else ""
city_name_two = reviews_queried_two["location"].iloc[0] if attraction_box_two[0] != "All" else ""
governorate_name_two = reviews_queried_two["governorate"].iloc[0] if attraction_box_two[0] != "All" else ""

# *****************************************************************************************************#

tab1, tab2, tab3, tab4, tab5  = st.tabs(["General Info", "Geographic Distribution of Reviewers",\
                                   "Timeline of Reviews", "Percentage of Ratings in Reviews",
                                   "Location of Attractions in Lebanon"])

# *****************************************************************************************************#

with tab1:

    title_1 = f"Total Ratings, Average Rating, and Written Review Number of {attraction_name_one} and {attraction_name_two}: " if (attraction_box_one[0] != "All" and attraction_box_two[0] != "All") else ""
    st.subheader(title_1)

    attraction_one, attraction_two = st.columns(2)
    # Reviews
    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        total_ratings = reviews_queried_one["total_ratings"].iloc[0] if attraction_box_one[0] != "All" else ""
        overall_avg_rating = reviews_queried_one["overall_rating"].iloc[0] if attraction_box_one[0] != "All" else ""

        tr_info = display_info("Total Number of Ratings", total_ratings, right_unit="📄") if attraction_box_one[
                                                                                                     0] != "All" else ""
        ov_rating_info = display_info("Overall Average Rating", overall_avg_rating, right_unit="⭐") if \
        attraction_box_one[0] != "All" else ""


        written_reviews_number = reviews_queried_one["written_reviews_number"].iloc[0] if attraction_box_one[
                                                                                              0] != "All" else ""
        written_reviews_info = display_info("Total Number of Written Reviews", written_reviews_number,\
                                                right_unit="📄") if attraction_box_one[0] != "All" else ""

with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        total_ratings = reviews_queried_two["total_ratings"].iloc[0] if attraction_box_two[0] != "All" else ""
        overall_avg_rating = reviews_queried_two["overall_rating"].iloc[0] if attraction_box_two[0] != "All" else ""

        tr_info = display_info("Total Number of Ratings", total_ratings, right_unit="📄") if attraction_box_two[
                                                                            0] != "All" else ""


        ov_rating_info = display_info("Overall Average Rating", overall_avg_rating, right_unit="⭐") if \
            attraction_box_two[0] != "All" else ""


# *****************************************************************************************************#

with tab2:
    st.subheader("Nationalities of Trip Advisor Users who Reviewed about the Attraction:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""



        df_nationalities = get_reviewers_nationalities_df(reviews_queried_one)

        with st.container():

            df_grouped = df_nationalities.groupby(["user_country"])["users_count"].count().reset_index(
                    name="users_count")
            countries = pd.read_csv("countries.csv")
            df_grouped_final = pd.merge(df_grouped, countries, on='user_country')
            map_lat = df_grouped_final.latitude
            map_long = df_grouped_final.longitude
            df_grouped_final = df_grouped_final.set_index('users_count')
            title = "<b>Nationalities of Trip Advisor Users who Reviewed about Lebanon</b>" if attraction_box_one[0] == "All" else f"<b>Nationalities of Trip Advisor Users who Reviewed about {attraction_name_one}</b>"

            map = display_world_map(df_grouped_final,
                                        title,
                                        np.absolute((df_grouped_final.index)), 'user_country')
            st.plotly_chart(map, use_container_width=True)


    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""


        st.info("Google Reviews does not share data about the nationalities of its reviewers.")

# *****************************************************************************************************#

with tab3:
    st.subheader("Time Series Graph of Reviews According to Years: ")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        sa_time_plot = plot_time_series_count(reviews_queried_one )
        st.plotly_chart(sa_time_plot, use_container_width=True)


    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        sa_time_plot = plot_time_series_count_google_reviews(reviews_queried_two)
        st.plotly_chart(sa_time_plot, use_container_width=True)

# *****************************************************************************************************#

with tab4:

    st.subheader("Distribution of Reviews per Rating: ")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.markdown(f'**{attraction_name_one}**')
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        ratings_distribution = reviews_queried_one['review_rating'].value_counts().rename_axis(
            ['review_rating']).reset_index(name='counts')

        # Plotting  pie chart for ratings
        fig_pie = px.pie(values=ratings_distribution.counts, names=ratings_distribution.review_rating,
                         title='Rating Distribution of Reviews',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        ratings_distribution = reviews_queried_two['review_rating'].value_counts().rename_axis(
            ['review_rating']).reset_index(name='counts')

        # Plotting  pie chart for ratings
        fig_pie = px.pie(values=ratings_distribution.counts, names=ratings_distribution.review_rating,
                         title='Rating Distribution of Reviews',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

# *****************************************************************************************************#

with tab5:
    st.subheader("Location of Attractions in Lebanon:")

    attraction_one, attraction_two = st.columns(2)

    with attraction_one:
        st.write(f'<b>{attraction_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_one}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_one}<b>', unsafe_allow_html = True)
        sep1 = st.markdown("""---""") if (attraction_box_one[0] != "All") else ""

        fig_one = display_map_lebanon(reviews_queried_one)
        st.plotly_chart(fig_one)



    with attraction_two:
        st.write(f'<b>{attraction_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{city_name_two}<b>', unsafe_allow_html = True)
        st.write(f'<b>{governorate_name_two}<b>', unsafe_allow_html = True)
        sep2 = st.markdown("""---""") if (attraction_box_two[0] != "All") else ""

        fig_two = display_map_lebanon(reviews_queried_two)
        st.plotly_chart(fig_two)

# *****************************************************************************************************#