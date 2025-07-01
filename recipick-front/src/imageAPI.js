import axios from 'axios';

// Using a class to encapsulate the Image API functionality
// This allows for better organization and potential future expansion of the API functionality.
// The class can be instantiated, and methods can be called to fetch images based on queries.
// The class also includes error handling and checks to ensure the API is initialized before making requests.
export class ImageAPI {
  _imageAPI = null;

  constructor() {
    const key = import.meta.env.VITE_GOOGLE_API_KEY;
    const cx = import.meta.env.VITE_GOOGLE_CX;

    if (!(key && cx)) {
      console.error('Google API key and Custom Search Engine ID (CX) must be set in environment variables for ImageApi to work.');
      return;
    }

    this._imageAPI = axios.create({
      baseURL: 'https://www.googleapis.com/customsearch/v1',
      headers: {
        'Content-Type': 'application/json',
      },
      params: {
        key,
        cx
      },
    });
  }

  async fetchFoodImage(query) {
    if (!this._checkImageAPI()) return null; // Ensure the API is initialized before making requests

    if (!query || typeof query !== 'string' || query.trim() === '') {
      console.error('Invalid query:', query);
      return null; // Return null if the query is invalid
    }

    try {
      const { data } = await this._imageAPI.get('', {
        params: {
          q: query,
          searchType: 'image',
          num: 1,
        },
      });

      const imageResults = data.items;
      if (imageResults && imageResults.length > 0) {
        // Using thumbnailLink for better performance
        // as it provides a smaller image size compared to link
        // and is suitable for displaying in the UI.
        return imageResults[0].image.thumbnailLink; // Return the thumbnail link of the first image
      }

    } catch (error) {
      console.error('Error fetching food image:', error);
    }
    return null;
  }

  async _checkImageAPI() {
    if (this._imageAPI == null) {
      console.error('ImageApi is not initialized. Check your environment variables.');
      return false;
    }
    return true; // Return true if the API is initialized
  }
}
