# Lunatic Rave 2 Score Scraper 
### [Live Version](https://lr2ir-top-scores.herokuapp.com/)

This app scrapes score data from [Lunatic Rave 2's Score Database website](http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&bmsid=1031). It cleans and formats the scraped HTML data into a readable pandas dataframe format. The intended goal was to be able to view charts for BMS songs faster than having to open BeMusicSeeker.

Users can view the top rankings for any song on the website. The app will dynamically plot a top 25 scores graph for any ranking page using Matplotlib's data visualization methods.

Supports searching by name/artist, bms/bml/bme/pms files, LR2 ID, or song MD5.

It also supports several popular tables and has links to view the charts themselves.

Please message me on Discord at Blaze#1163 if you have any requests or feedback.

## Requirements
- flask
- pandas
- matplotlib
- bs4

## Screenshots
![1](https://user-images.githubusercontent.com/45186205/160724705-adf5d122-a67a-4943-888b-50058c7bd2db.png)
![2](https://user-images.githubusercontent.com/45186205/160724098-3b9476f4-9514-42dd-aee0-583a7bc32722.png)
![3](https://user-images.githubusercontent.com/45186205/160724100-2d250855-c972-4c78-9bee-8053c1fb940f.png)
