# Chicago Crime Data Visualization | R
This project was inspired out of a curiosity for assessing crime rates throughout Chicago’s various different neighborhoods. Using Tableau, R statistical analysis, and the 2012 – 2016 crime data from Kaggle, my team and I investigated the different types of crimes that occurred, the arrest rates, and the frequency and time of year they took place. This investigation covered 3 different techniques for analyzing the crime dataset: exploratory graphs (dot and bar charts and treemaps), time series (line plots and heat maps), and geographical graphs.

![False Color Geographical Heatmap- chicago crime](/Data%20Visualization%20-%20Chicago%20Crime%20%7C%20R/geographical%20graph%20with%20false%20color%20heat%20map.png)

* Crime Hot Spots: downtown, southside, and area between Oak Park and Downtown
* Overall crime in Chicago has declined from 2012 to 2016
* Top crime types committed were theft and battery
* Recurring high crime rate during the summer periond (June - August) every year

### Script

```R
library(ggplot2)

#load data
crime1617<- read.csv("Chicago_Crimes_2012_to_2017.csv")
head(crime1617)

#######################Preproccessing###################################

#seperate the date colume to day, month, year
library(lubridate)
crime1617$Date <- as.Date(crime1617$Date, "%m/%d/%Y %I:%M:%S %p")
crime1617$Day <- factor(day(as.POSIXlt(crime1617$Date, format="%m/%d/%Y %I:%M:%S %p")))
crime1617$Month <- factor(month(as.POSIXlt(crime1617$Date, format="%m/%d/%Y %I:%M:%S %p"), label = TRUE))
crime1617$Year <- factor(year(as.POSIXlt(crime1617$Date, format="%m/%d/%Y %I:%M:%S %p")))
crime1617$Weekday <- factor(wday(as.POSIXlt(crime1617$Date, format="%m/%d/%Y %I:%M:%S %p"), label = TRUE))

#missing values?
colSums(is.na(crime1617))
#remove rows containg missing values
crime_cleaned<- na.omit(crime1617)
colSums(is.na(crime_cleaned))

#remove year 2017 due to lack of observation (preventing distoration)
crime_cleaned <- crime_cleaned[crime_cleaned$Year!='2017',]

#overview of columns
str(crime_cleaned)
head(crime_cleaned)




#write.table(crime_cleaned,"crime_cleaned.txt",sep="\t",row.names=FALSE)



##################### Preproccessing done ###########################

#exploratory
library(gridExtra)
library(plyr)

# barplot by type
type_crime = arrange(count(crime_cleaned,c("Primary.Type")),(desc(freq)))

bar_type=ggplot(data=type_crime, aes(x=reorder(Primary.Type,freq),y=freq/1000)) +
  geom_bar(colour="black", fill="blue",stat = "identity") +
  ylab('Count in thousands')+coord_flip()+xlab("crime type")+ggtitle("crime type")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))



# barplot by Location
location_crime = arrange(count(crime_cleaned,c("Location.Description")),(desc(freq)))

bar_loc=ggplot(data=location_crime[1:20,], aes(x=reorder(Location.Description,freq),y=freq/1000)) +
  geom_bar(colour="black", fill="green",stat = "identity") +
  ylab('Count in thousands')+coord_flip()+xlab("crime location")+ggtitle("Top 20 crime location")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))


grid.arrange(bar_type,bar_loc, ncol = 2)

# barplot by arrest
arrest_crime = arrange(count(crime_cleaned,c("Arrest")),(desc(freq)))

bar_arrest=ggplot(data=arrest_crime, aes(x=reorder(Arrest,freq),y=freq/1000,fill=Arrest)) +
  geom_bar(stat = "identity") +
  ylab('Count in thousands')+coord_flip()+xlab("Arrest")+ggtitle("Arrest or not")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))+
  geom_text(aes(label = sprintf("%.2f%%", freq/sum(freq) * 100)), 
            vjust = -.5)


# barplot by Domestic
dos_crime = arrange(count(crime_cleaned,c("Domestic")),(desc(freq)))

bar_Domestic=ggplot(data=dos_crime, aes(x=reorder(Domestic,freq),y=freq/1000,fill=Domestic)) +
  geom_bar(stat = "identity") +
  ylab('Count in thousands')+coord_flip()+xlab("Domestic")+ggtitle("Domestic or not")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))+
  geom_text(aes(label = sprintf("%.2f%%", freq/sum(freq) * 100)), 
            vjust = -.5)
                                                                                                                                                                            



grid.arrange(bar_arrest,bar_Domestic, ncol = 2)


##technique 1 

# dot Plot by type

library(ggplot2)
library(scales)
theme_set(theme_classic())

type_crime = arrange(count(crime_cleaned,c("Primary.Type")),(desc(freq)))

dot_type=ggplot(data=type_crime[1:10,], aes(x=reorder(Primary.Type,freq),y=freq/1000))  + 
  geom_point(col="black", size=3, alpha= 0.7) +   # Draw points
  geom_segment(aes(x=Primary.Type, 
                   xend=Primary.Type, 
                   y=min(freq/1000), 
                   yend=max(freq/1000)), 
               linetype="dashed", 
               size=0.1) +   # Draw dashed lines
  labs(title="Dot Plot: Top 10 crime type", 
       subtitle="crime type Vs Count in thousand", 
       caption="source: Crime") +  
  coord_flip()


# dot Plot by location

location_crime = arrange(count(crime_cleaned,c("Location.Description")),(desc(freq)))
dot_loc=ggplot(data=location_crime[1:10,], aes(x=reorder(Location.Description,freq),y=freq/1000))  + 
  geom_point(col="black", size=3, alpha= 0.7) +   # Draw points
  geom_segment(aes(x=Location.Description, 
                   xend=Location.Description, 
                   y=min(freq/1000), 
                   yend=max(freq/1000)), 
               linetype="dashed", 
               size=0.1) +   # Draw dashed lines
  labs(title="Dot Plot: Top 10 crim location", 
       subtitle="crime type Vs Count in thousand", 
       caption="source: Crime") +  
  coord_flip()


grid.arrange(dot_type, dot_loc, ncol = 2)

# top 20 arrest rate location 
ar_loc = arrange(count(crime_cleaned,c("Location.Description","Arrest")),(desc(freq)))
library(dplyr)

ar_locG=ar_loc%>%group_by(Location.Description)%>%
  mutate(per=paste0(round(freq/sum(freq)*100, 2), "%")) %>% 
  ungroup
ar_locGT =ar_locG[ar_locG$Arrest == "True",]


ar_locGT$per=as.numeric(sub("%", "", ar_locGT$per))
ar_locGT = arrange(ar_locGT,(desc(per)))
head(ar_locGT)
bar_ar_loc=ggplot(data=ar_locGT[1:20,], aes(x=reorder(Location.Description,per),y=per)) +
  geom_bar(colour="black", fill="black",stat = "identity") +
  ylab('arrest rate')+coord_flip()+xlab("crime location")+ggtitle("Top 20 arrest rate by location")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))

bar_ar_loc=bar_ar_loc+ scale_y_continuous(limits = c(0, 100))



# top 20 nonarrest rate location 


ar_locGF =ar_locG[ar_locG$Arrest == "False",]


ar_locGF$per=as.numeric(sub("%", "", ar_locGF$per))
ar_locGF = arrange(ar_locGF,(desc(per)))
head(ar_locGF)
bar_F_Loc=ggplot(data=ar_locGF[1:20,], aes(x=reorder(Location.Description,per),y=per)) +
  geom_bar(colour="black", fill="black",stat = "identity") +
  ylab('non arrest rate')+coord_flip()+xlab("crime location")+ggtitle("Top 20 non arrest rate by location")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))

bar_F_loc=bar_F_Loc+ scale_y_continuous(limits = c(0, 100))




grid.arrange(bar_ar_loc,bar_F_loc, ncol = 2)





#arrest top 10 type


ar_type = count_(crime_cleaned,c("Primary.Type","Arrest"))

ar_typeG=ar_type%>%group_by(Primary.Type)%>%
  mutate(per=paste0(round(n/sum(n)*100, 2), "%")) %>% 
  ungroup
ar_typeGT =ar_typeG[ar_typeG$Arrest == "True",]
head(ar_typeGT)

ar_typeGT$per=as.numeric(sub("%", "", ar_typeGT$per))
ar_typeGT = arrange(ar_typeGT,(desc(per)))
head(ar_typeGT)
bar_ar_typeGT=ggplot(data=ar_typeGT[1:20,], aes(x=reorder(Primary.Type,per),y=per)) +
  geom_bar(colour="black", fill="black",stat = "identity") +
  ylab('arrest rate')+coord_flip()+xlab("crime type")+ggtitle("Top 20 arrest rate by type")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))

bar_ar_typeGT=bar_ar_typeGT+ scale_y_continuous(limits = c(0, 100))
bar_ar_typeGT



# top 20 nonarrest rate type 

ar_typeGF =ar_typeG[ar_typeG$Arrest == "False",]
head(ar_typeGF)

ar_typeGF$per=as.numeric(sub("%", "", ar_typeGF$per))
ar_typeGF = arrange(ar_typeGF,(desc(per)))
head(ar_typeGF)
bar_ar_typeGF=ggplot(data=ar_typeGF[1:20,], aes(x=reorder(Primary.Type,per),y=per)) +
  geom_bar(colour="black", fill="black",stat = "identity") +
  ylab('non arrest rate')+coord_flip()+xlab("crime type")+ggtitle("Top 20 non-arrest rate by type")+theme(plot.title = element_text(color="Black", size=14, face="bold.italic"))

bar_ar_typeGF=bar_ar_typeGF+ scale_y_continuous(limits = c(0, 100))
bar_ar_typeGF



grid.arrange(bar_ar_typeGT,bar_ar_typeGF, ncol = 2)



##technique 2 
#line plot by Date
library(plyr)
library(scales)
daily_crime = count_(crime_cleaned,"Date")
dCrime_lineplot = ggplot(data = daily_crime, aes(x = Date, y = n)) + ylab('count') + xlab('Date')  + geom_line(col='blue')
dCrime_lineplot = dCrime_lineplot+scale_x_date(date_breaks="1 years",labels = date_format("%m/%d/%Y"),limits = c(as.Date("2012-01-01"), as.Date("2016-12-31")))
dCrime_lineplot = dCrime_lineplot+theme(axis.ticks.x=element_blank(),axis.text.x = element_text(angle = 45, hjust = 1)) +ggtitle("Daliy Crime from 2012-2017")
dCrime_lineplot

#with mv smotthing line
f = rep(1/60, 60)
f
daily_crime$mAve = filter(daily_crime$n, f, sides=1)

dCrime_lineplot = ggplot(data = daily_crime, aes(x = Date, y = n)) + ylab('count') + xlab('Date')  + geom_line(color="black",alpha=0.5)
dCrime_lineplot = dCrime_lineplot+scale_x_date(date_breaks="1 years",labels = date_format("%m/%d/%Y"),limits = c(as.Date("2012-01-01"), as.Date("2016-12-31")))
dCrime_lineplot = dCrime_lineplot+theme(axis.ticks.x=element_blank(),axis.text.x = element_text(angle = 45, hjust = 1)) +ggtitle("Daliy Crime from 2012-2017")
dCrime_lineplot + geom_line(aes(x= Date, y=mAve), color="red")



#time plot by top 3 crime type yearly
ggplot(df,aes(x=x,y=y,group=col,colour=factor(col))) + geom_line()

dailytype_crime = count_(crime_cleaned,c("Year","Primary.Type"))
top3crimtype = subset(dailytype_crime, Primary.Type=="THEFT" | Primary.Type=="BATTERY"| Primary.Type=="CRIMINAL DAMAGE")
ggplot(top3crimtype,aes(x = Year, y = n,group=Primary.Type,colour=Primary.Type)) + geom_line()








#heat map

Monthly_crime =count_(crime_cleaned,c("Month","Year"))

crimes <- ggplot(Monthly_crime, aes(Year, Month, fill = n)) +geom_tile(size = 1, color = "white")  +ggtitle("Crimes by Year and Month(2012-2016)")
crimes


##tree map
library(treemap)

crimemap =count_(crime_cleaned,c("Primary.Type","Location.Description"))


treemap(crimemap, 
        index=c("Primary.Type", "Location.Description"),
        vSize="n", 
        type="index")

##technique 3 :geographical crime at 2016-2017



library(ggmap)
install.packages("ggmap", type = "source")
chicago <- get_map(location = 'chicago', zoom = 11)
ggmap(chicago)

#subset for only 2016
crime_cleaned=subset(crime_cleaned,crime_cleaned$Year==2016)

#geographical heat map overall
LatLonCounts <- as.data.frame(table(round(crime_cleaned$Longitude,2), round(crime_cleaned$Latitude,2)))
head(LatLonCounts)
str(LatLonCounts)

LatLonCounts$Long <- as.numeric(as.character(LatLonCounts$Var1))
LatLonCounts$Lat <- as.numeric(as.character(LatLonCounts$Var2))


LatLonCounts_cleaned <- subset(LatLonCounts, Freq > 0)
ggmap(chicago) + geom_tile(data = LatLonCounts_cleaned, aes(x = Long, y = Lat,fill = Freq),alpha=0.7)+ theme(axis.title.y = element_blank(), axis.title.x = element_blank())+labs(title = "2016 Overall Crime geographical heat map") + scale_fill_gradient(low = "green", high = "red") +scale_alpha(range = c(0, 0.3), guide = FALSE)

#take a look at top 2 crime type
levels(crime_cleaned$Primary.Type)
#geographical heatmap for theft and BATTERY
#theft
theft=subset(crime_cleaned,crime_cleaned$Primary.Type=="THEFT")

LatLonCounts_theft <- as.data.frame(table(round(theft$Longitude,2), round(theft$Latitude,2)))


LatLonCounts_theft$Long <- as.numeric(as.character(LatLonCounts_theft$Var1))
LatLonCounts_theft$Lat <- as.numeric(as.character(LatLonCounts_theft$Var2))


LatLonCounts_theft_cleaned <- subset(LatLonCounts_theft, Freq > 0)
a=ggmap(chicago) + geom_tile(data = LatLonCounts_theft_cleaned, aes(x = Long, y = Lat, fill = Freq), alpha=0.6)+ theme(axis.title.y = element_blank(), axis.title.x = element_blank())+labs(title = "2016 geographical heat map for Theft") 
a=a+ scale_fill_gradient(low = "green", high = "red") 
a

#battery
battery=subset(crime_cleaned,crime_cleaned$Primary.Type=="BATTERY")

LatLonCounts_tbattery <- as.data.frame(table(round(battery$Longitude,2), round(battery$Latitude,2)))


LatLonCounts_tbattery$Long <- as.numeric(as.character(LatLonCounts_tbattery$Var1))
LatLonCounts_tbattery$Lat <- as.numeric(as.character(LatLonCounts_tbattery$Var2))


LatLonCounts_tbattery_cleaned <- subset(LatLonCounts_tbattery, Freq > 0)
b=ggmap(chicago) + geom_tile(data = LatLonCounts_tbattery_cleaned, aes(x = Long, y = Lat, fill = Freq), alpha = 0.6)+ theme(axis.title.y = element_blank(), axis.title.x = element_blank())+labs(title = "2016 geographical heat map for battery") 
b=b+ scale_fill_gradient(low = "green", high = "red") 
b







#take look at some crime type we are interested
#geographical heatmap for homicide
HOMICID=subset(crime_cleaned,crime_cleaned$Primary.Type=="HOMICIDE")

LatLonCounts_HOMICID <- as.data.frame(table(round(HOMICID$Longitude,2), round(HOMICID$Latitude,2)))


LatLonCounts_HOMICID$Long <- as.numeric(as.character(LatLonCounts_HOMICID$Var1))
LatLonCounts_HOMICID$Lat <- as.numeric(as.character(LatLonCounts_HOMICID$Var2))


LatLonCounts_HOMICID_cleaned <- subset(LatLonCounts_HOMICID, Freq > 0)
c=ggmap(chicago) + geom_tile(data = LatLonCounts_HOMICID_cleaned, aes(x = Long, y = Lat, fill = Freq), alpha = 0.6)+ theme(axis.title.y = element_blank(), axis.title.x = element_blank())+labs(title = "2016 geographical heat map for HOMICIDE") 
c=c+ scale_fill_gradient(low = "green", high = "red") 
c


#geographical heatmap for ROBBERY

ROBBERY=subset(crime_cleaned,crime_cleaned$Primary.Type=="ROBBERY")

LatLonCounts_ROBBERY <- as.data.frame(table(round(ROBBERY$Longitude,2), round(ROBBERY$Latitude,2)))


LatLonCounts_ROBBERY$Long <- as.numeric(as.character(LatLonCounts_ROBBERY$Var1))
LatLonCounts_ROBBERY$Lat <- as.numeric(as.character(LatLonCounts_ROBBERY$Var2))


LatLonCounts_ROBBERY_cleaned <- subset(LatLonCounts_ROBBERY, Freq > 0)
d=ggmap(chicago) + geom_tile(data = LatLonCounts_ROBBERY_cleaned, aes(x = Long, y = Lat, fill = Freq), alpha = 0.6)+ theme(axis.title.y = element_blank(), axis.title.x = element_blank())+labs(title = "2016 geographical heat map for ROBBERY") 
d=d+ scale_fill_gradient(low = "green", high = "red") 
d


grid.arrange(a, b,c,d, ncol = 2, nrow=2)



```
