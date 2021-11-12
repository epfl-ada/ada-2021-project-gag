# Influence of politics in sport media
 
# Abstract : 
The goal of this project is to assess the link between politics and sport media. It is well known that media and politics are very closely linked and that certain media have a clear inclination towards certain parties. Politicians use the media as a tool to make their popularity grow. However certain media focus on subjects which are unrelated to politics, like sport. But are they really not influenced by politics and politicians ? Indeed, it might offer an interesting opportunity for politicians to reach a new public and discreetly increase their popularity among them. The idea is therefore to study to what extent this phenomenon is present according to certain criteria such as the media, the sport, the country or over time. Also, if a political current, a party, a politician or a country in particular are more present than others in the sports media. 

# Research questions : 
To explore this subject the following questions can be assessed : 
- How much of the sport quotes among each media is politics related? 
- How does this phenomenon evolve over time? For instance, does it increase before elections ? 
- Which political parties or politicians are the most present in the sports quotes?  
- What is the distribution of the political tendency of the political parties present in the sports quotes (going from extreme right to extreme left)? 
- What is the distribution of the political parties present for a specific country? 

# Additional datasets : 
To answer those questions, additional dataset are necessary or could be useful. The following list shows what additional dataset are interesting in this study :
Additional metadata about the speakers in the Quotebank dataset provided in the file named speaker_attributes.parquet 
Extra data from Wikidata : Periods of membership in each party if a person is assigned to more than one party + Description of each party, political orientation + country of each media
These two types of data have already been handled in this second Milestone, showing that we are capable of handling it, in terms of size and in terms of finding the data.

# Methods : 
The data are processed by chunks given their size to avoid reaching the memory limit. This slightly complicates the code but allows to process any dataset size.

*Data processing :*


1.   Identify quotes related to sport in each year and store them as a CSV : several methods are possible to filter sports quotes. One way would be to use machine learning algorithm to filter the quotes based on their content. Another is to use the url of the source to look for sports media or urls containing the word “sport”. This last method has been used so far and worked well given that “sports” usually appears in the url because the article comes from the sport section. From now on, the rest of the work is done using this new dataset.
2.   Investigate the media who published the quotes : again, looking at the URL and using the library TLD, one can extract the domain name which indicates the media publishing the quote.
3. Extract the speakers from these quotes
4. Extract the speakers that are assigned to a political party : using the additional dataset allows to find which speakers are related to politics.
5. Extract the party of the speaker when he/she said the quote
6. Extract the orientation of the parties

*Analysis :*
1. Extract percentage of sport quotes
2. Display percentage of sport quotes from politicians over media, over parties, over time, over sports, over teams and over players
3. Display the main political parties or politicians speakers of sport quotes
4. Display distribution of the political tendency of the political parties
5. Display distribution by country of the political parties

# Timeline : 
Until now the goal was to verify if this analysis is feasible by exploring the data and verifying that the methods work and that there is enough data. Now we will be able to properly start the analysis based on this first work and integrate the feedback of this milestone. Afterwards, it will be necessary to interpret the results obtained. Finally, clean up and standardize the code and create the datastory.

*5 Nov to 12 Nov :* Data preprocessing from task 1 to 4 + code to produce initial analysis data

*12 Nov to 3 Dec :* Data preprocessing from task 5 and 6 + code to produce analysis data

*3 Dec to 10 Dec :* Analysis data results interpretation + start the datastory 

*10 Dec to 17 Dec :* Clean up and standardize the code + finish the datastory

# Organization within the team :

*5 Nov to 12 Nov :* 
- Data processing 1 and 2 : Etienne and Nicolas
- Data processing 3 and 4 : Maxime and Francesca

*12 Nov to 3 Dec :* 
- Data processing 5 and 6 : Maxime and Francesca
- Analysis 1, 2 and 3 : Etienne and Nicolas

*3 Dec to 10 Dec :*
- Data story and analysis : Etienne and Nicolas
- Analysis 4 and 5 : Maxime and Francesca

*10 Dec to 17 Dec :* 
- Data story and analysis : Maxime and Francesca
- Clean up, verifications, rereading : Etienne and Nicolas

# Notebooks description :
**sports_quotes :** Imports data from the Quotebank and extracts quotes from sport media and sports sections of more general media

**Sources :** Analysis of the distribution of the media publishing sports quotes.

**Party_distribution :**  Import data from speaker_attributes.parquet. For each year, extract politicians which are speakers of sport quotes and their political parties. First analysis of the distribution of sport quotes over political parties. 

# Questions for TAs : 
We tried to stay very broad in the questions that we could ask ourselves, but we may have cited too many or some may be too difficult. Even though we have a pretty clear idea of what we want to do and how we want to do it, we though it was more interesting to put a bit more here so that you can give your feedback on all our ideas before we discard some. So we would like your opinion on which are the most interesting aspects to deal with.
