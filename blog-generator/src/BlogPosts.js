import React, { useState } from 'react';

const BlogPosts = () => {
  // eslint-disable-next-line
  const [selectedCategory, setSelectedCategory] = useState('');
  const [blogPost, setBlogPost] = useState(null); // Store the generated blog post

  // Categories
  const categories = {
    0: 'Power and Connectivity Accessories',
    1: 'Amazon Devices and Media Equipment',
    2: 'Computing and Mobile Devices',
    3: 'Home and Office Products',
    4: 'Carrying and Storage Accessories',
    5: 'Audio Equipment and Accessories',
  };

  // Function to fetch blog post for the selected category
  const fetchBlogPost = async (category) => {
    console.log('Fetching blog post for category:', category);
    try {
      const response = await fetch(
        'https://dzym1rm5tj.execute-api.eu-north-1.amazonaws.com/staging/api/generate_blog_post',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ category }),
        }
      );
      const data = await response.json();
      setBlogPost(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const safelyGetSection = (content, startMarker, endMarker) => {
    if (!content) return '';
    const start = content.split(startMarker)[1];
    if (!start) return '';
    const end = start.split(endMarker)[0];
    return end ? end.trim() : '';
  };

  return (
    <div>
      {/* Centered header and dropdown */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          marginBottom: '20px',
        }}
      >
        <h1>Product Blog Posts</h1>

        {/* Dropdown to select category */}
        <div>
          <label>Select Category:</label>
          <select
            onChange={(e) => {
              const selected = e.target.value;
              setSelectedCategory(selected);
              fetchBlogPost(selected); // Trigger the API call here
            }}
          >
            <option value="">Select a category</option>
            {Object.values(categories).map((category, idx) => (
              <option key={idx} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Display the blog post */}
      {blogPost && blogPost.blog_post && (
        <div className="blog-post">
          <h2>{blogPost.product_name}</h2>
          <section>
            <h3>Product Overview</h3>
            <p>
              {safelyGetSection(
                blogPost.blog_post,
                '## Product Overview',
                '## Key Features'
              )}
            </p>
          </section>

          <section>
            <h3>Key Features</h3>
            <p>
              {safelyGetSection(
                blogPost.blog_post,
                '## Key Features',
                '## Pros'
              )}
            </p>
          </section>

          <section>
            <h3>Pros</h3>
            <ul>
              {safelyGetSection(blogPost.blog_post, '## Pros', '## Cons')
                .replace(/[[\]']+/g, '') // Remove brackets and single quotes
                .split('\n- ')
                .map((pros, idx) => (
                  <li key={idx}>{pros}</li>
                ))}
            </ul>
          </section>

          <section>
            <h3>Cons</h3>
            <ul>
              {safelyGetSection(blogPost.blog_post, '## Cons', '## Conclusion')
                .replace(/[[\]']+/g, '') // Remove brackets and single quotes
                .split('\n- ')
                .map((cons, idx) => (
                  <li key={idx}>{cons}</li>
                ))}
            </ul>
          </section>

          <section>
            <h3>Conclusion</h3>
            <p>{safelyGetSection(blogPost.blog_post, '## Conclusion', '')}</p>
          </section>
        </div>
      )}
    </div>
  );
};

export default BlogPosts;
