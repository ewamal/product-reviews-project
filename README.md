### Product Review Generation using GPT-2

#### Overview

This project is aimed at building an NLP-powered platform for analyzing customer reviews, categorizing products, and generating blog-style summaries. Using existing pre-trained language models, the system performs sentiment analysis, product clustering, and generates informative summaries

#### Deployment

The backend is deployed on AWS and handles the blog post generation based on the product category.

The frontend is a React-based web app deployed on Netlify. Accessible [here](https://storied-twilight-5e4414.netlify.app/)

#### Project Organization

---

```
├── README.md <- The top-level README.
├── data
│   ├── generated_blog_posts.csv <- The final, generated blog posts
│  
├── notebooks <- Jupyter notebooks.
│
├── backend
├── blog-generator <- frontend
├── requirements.txt <- The requirements file for reproducing the analysis environment
```

---

## References

- https://huggingface.co/gpt2
- https://huggingface.co/ewamal/gpt2-post-generation
