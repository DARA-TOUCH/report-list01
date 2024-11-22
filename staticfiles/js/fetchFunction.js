fetch('https://jsonplaceholder.typicode.com/posts')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();  // Parse the JSON response
  })
  .then(data => {
    console.log(data);  // Handle the data
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });