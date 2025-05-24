import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
# Load dataset
df = pd.read_csv('C:/Users/Hemanth/OneDrive/Shiva/Play Store Data.csv')#Modify the path as your wish
# Filter for Health & Fitness category
health_apps = df[(df['Category'] == 'HEALTH_AND_FITNESS')]
# Simulated 5-star reviews for demonstration
simulated_reviews = [
    "Great app, easy to navigate and very helpful for managing my insurance.",
    "Absolutely love the features. Makes claims and doctor searches simple!",
    "Very intuitive design, fast loading, and useful health tracking features.",
    "Helpful support and all the information I need is right at my fingertips.",
    "Efficient, reliable, and constantly improving. Highly recommend this app!"
]
# Combine all reviews into one string
text = " ".join(simulated_reviews)
# Define stopwords including app-specific terms
custom_stopwords = set(STOPWORDS)
custom_stopwords.update(["app", "blue", "florida", "insurance", "features"])
# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white',stopwords=custom_stopwords, colormap='viridis').generate(text)
# Save the word cloud image
output_path = "C:/Users/Hemanth/OneDrive/Shiva/florida_blue_wordcloud.png" #Modify the path as your wish
wordcloud.to_file(output_path)
# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

print(f"Word cloud saved to {output_path}")
