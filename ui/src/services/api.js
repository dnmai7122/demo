/**
 * API Service for communicating with backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Fetch all topics from the backend
 * @returns {Promise<Array>} Array of topics
 */
export const fetchTopics = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/topics`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      return data.data;
    } else {
      throw new Error("Failed to fetch topics");
    }
  } catch (error) {
    console.error("Error fetching topics:", error);
    throw error;
  }
};

/**
 * Search topics by name
 * @param {string} query - Search query for topic name
 * @returns {Promise<Array>} Array of matching topics
 */
export const searchTopics = async (query) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/topics/search?query=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      return data.data;
    } else {
      throw new Error("Failed to search topics");
    }
  } catch (error) {
    console.error("Error searching topics:", error);
    throw error;
  }
};

/**
 * Fetch a single topic by ID
 * @param {number} topicId - The ID of the topic
 * @returns {Promise<Object>} Topic object
 */
export const fetchTopicById = async (topicId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/topics/${topicId}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      return data.data;
    } else {
      throw new Error("Failed to fetch topic");
    }
  } catch (error) {
    console.error("Error fetching topic:", error);
    throw error;
  }
};

/**
 * Fetch all lessons for a specific topic
 * @param {number} topicId - The ID of the topic
 * @returns {Promise<Array>} Array of lessons
 */
export const fetchLessonsByTopic = async (topicId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/topics/${topicId}/lessons`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      return data.data;
    } else {
      throw new Error("Failed to fetch lessons");
    }
  } catch (error) {
    console.error("Error fetching lessons:", error);
    throw error;
  }
};

/**
 * Fetch all lessons from the backend
 * @returns {Promise<Array>} Array of all lessons
 */
export const fetchAllLessons = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/lessons`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      return data.data;
    } else {
      throw new Error("Failed to fetch lessons");
    }
  } catch (error) {
    console.error("Error fetching all lessons:", error);
    throw error;
  }
};

/**
 * Fetch units (video content) for a specific lesson directly from Supabase
 * @param {number} lessonId - The ID of the lesson
 * @returns {Promise<Array>} Array of units with video content
 */
export const fetchUnitsByLesson = async (lessonId) => {
  try {
    const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
    const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;

    if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
      throw new Error(
        "Missing Supabase configuration. Please check your .env file."
      );
    }

    const response = await fetch(
      `${SUPABASE_URL}/rest/v1/unit?lesson_id=eq.${lessonId}&order=order_index.asc`,
      {
        headers: {
          apikey: SUPABASE_ANON_KEY,
          Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching units:", error);
    throw error;
  }
};

/**
 * Hybrid search for units by description
 * @param {string} query - Description of the sign language gesture
 * @param {number} topK - Number of results to return (default: 3)
 * @returns {Promise<Array>} Array of matching units
 */
export const searchUnitsByDescription = async (query, topK = 3) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/search/units`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      return data.data;
    } else {
      throw new Error("Failed to search units");
    }
  } catch (error) {
    console.error("Error searching units:", error);
    throw error;
  }
};
