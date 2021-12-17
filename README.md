# Influence of politics in sport media

The [data story](https://mdulon.github.io/ADA_GaG_Datastory/) of this study is available by clicking the link or copy pasting this URL : https://mdulon.github.io/ADA_GaG_Datastory/

## Abstract

The goal of this project is to assess the link between politics and sport media. It is well known that media and politics are very closely linked and that certain media have a clear inclination towards certain parties. Politicians use the media as a tool to make their popularity grow. However certain media focus on subjects which are unrelated to politics, like sport. But are they really not influenced by politics and politicians? Indeed, it might offer an interesting opportunity for politicians to reach a new public and discreetly increase their popularity among them. The idea is therefore to study to what extent this phenomenon is present according to certain criteria such as the media, the sport, the country or over time. Also, if a political current, a party, a politician or a country in particular is more present than others in the sports media. 


## Research questions

To explore this subject the following questions can be assessed: 
- How much of the sport quotes among each media is politics related? 
- How does this phenomenon evolve over time? For instance, does it increase before elections? 
- Which political parties or politicians are the most present in the sports quotes?
- What is the distribution of the political tendency of the political parties present in the sports quotes (going from extreme right to extreme left)? 
- What is the distribution of the political parties present for a specific country? 


## Additional datasets

To answer these questions, additional datasets are necessary or could be useful. The following list shows what additional dataset are interesting in this study :
- Additional metadata about the speakers in the Quotebank dataset provided in the file `speaker_attributes.parquet`
- Extra data from Wikidata: 
  - periods of membership in each party if a person is assigned to more than one party
  - description of each party and its political orientation
  - country of each media

These two types of data have already been handled in this second milestone, showing that we are capable of handling it, both in terms of size and in terms of finding the data.


## Methods 

The data is processed by chunks given their size to avoid reaching the memory limit. This slightly complicates the code but allows to process datasets of arbitrary sizes.

### Data processing

  1. Identify quotes related to sport in each year and store them as a `.csv`; several methods are possible to filter sports quotes. One way would be to use a machine learning algorithm to filter the quotes based on their content. Another is to use the url of the source to look for sports media or urls containing the word "sport". This last method has been used so far and worked well given that "sport" usually appears in the url due to the fact that the article comes from the sport section. From now on, the rest of the work is done using this new dataset
  2. Investigate the media who published the quotes: again, looking at the URL and using the library TLD, one can extract the domain name which indicates the media publishing the quote
  3. Extract the speakers from these quotes
  4. Extract the speakers that are assigned to a political party: using the additional dataset allows to find which speakers are related to politics
  5. Extract the party of the speaker when he/she said the quote
  6. Extract the orientation of the parties

### Analysis
  1. Extract percentage of sport quotes
  2. Display percentage of sport quotes from politicians over media, over parties, over time, over sports, over teams and over players
  3. Display the main political parties or politicians speakers of sport quotes
  4. Display distribution of the political tendency of the political parties
  5. Display distribution by country of the political parties


## Organization within the team

Each member was responsible for certain research questions and did both the notebook/code for it and the datastory about it. In addition, some members provided local support for specific tasks such as building the webpage or the wikidata query function. We met regularly to discuss about our difficulties and coordinate each other work. In the end, most of the work was spread in this manner :

- Nicolas : coded the query function for wikidata + study of the party + creation of the first preprocess to retrieve only sport quotes
- Fracesca : worked on the study of speakers occupation and party
- Maxime : worked on the topic analysis + webpage creation
- Etienne : worked on the media analysis and the time analysis
