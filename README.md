# Ebay prices of Sold Reference GPUs

<p align="center">
  <img width="700" height="432" src=/images/gpuprices.png>
</p>

Using selenium in python, I scraped the prices of sold reference GPUs off ebay into excel spreadsheets. I cleaned up the data in python and then visualized it using ggplot in R to make the graph above.

This project was inspired by [this](https://www.reddit.com/r/dataisbeautiful/comments/q9y3ne/oc_sale_prices_of_used_iphones/) post on /r/dataisbeautiful that I saw on the front page of reddit. I discovered that this was a sina plot and wanted to create my own graphic with this type of graph. The reddit post used the listing price of iphones on ebay, but I thought the price of completed sold items were more useful so I wanted to use that. I knew that graphics cards are being sold at a premium due to their shortage and so I want to see how much above MSRP graphics cards are being sold on Ebay. Reference GPUs are graphics cards manufactured by NVIDIA and AMD themselves. I decided to only look at reference cards for the most recent GPU generation as looking at every brand that makes multiple GPUs would have taken a lot longer. A few comments speculated about how the data was collected as the poster did not specify. The two main sources was using Ebay's API and webscraping. I decided to try using Ebay API's first.

## Using Ebay API and its limits
After creating an ebay developer account and applying for production API keys, I followed [this](https://www.youtube.com/watch?v=Ma_eLdobmlM) wonderful tutorial by Python 360. Using [ebaySDK](https://github.com/timotheus/ebaysdk-python) to make requests, I was able to sucessfully retrieve listings of GPUs. By specifying aspect filters and item filters in the parameters of my request, I retrieved the listing price of only reference GPUs. However, this is when I ran into a bit of a problem. In turns out that Ebay's API was only able to return current listings, and not completed sold listings. There was a parameter in SoldItemsOnly that I could specify for item filter, but it was only a placeholder that was not functional. You used to be able to specify findCompletedItems in the request, but this call is depreciated and no longer useable. There exists a marketplace API, but in order to gain access you had to apply for business approval. 
