# Idea Document for Video API with Redis Caching
### Design Choices
This project involves building a Django-based API for serving paginated video content, with a focus on performance, scalability, and ensuring a smooth user experience for the fashion app's home screen.

1) API Design Using APIView:
APIView was used to maintain full control over the request-response lifecycle, ensuring flexibility for custom logic (such as cache control, pagination, etc.).
This ensures a clean separation of concerns with well-structured, maintainable code while adhering to REST principles.

2) Pagination for Scalable Content Delivery:
PageNumberPagination from DRF was implemented to handle paginated responses. It fetches only a limited number of video records per request, ensuring the API is scalable for large datasets. This improves performance by avoiding the need to load all video records at once, which is crucial as the number of videos grows.
The pagination logic allows for easy customization of page size via the query parameters, providing flexibility to the client for controlling data volumes.

3) Redis Caching for Performance:
Redis was used as a caching layer to reduce database queries and improve response times. The video data is cached based on the requested page to optimize performance for frequently accessed data.
The caching implementation ensures that content updates (additions or deletions of videos) are reflected in real-time, as the cache is invalidated through Django signals when changes occur in the database.

### Performance and Scalability

1) Efficient Data Querying:
    a) *Paginated Queries*: By leveraging DRF’s PageNumberPagination, only the required subset of video records is retrieved from the database for each request. This reduces memory overhead and optimizes response time for users requesting specific pages.
    b) *Optimized Querysets*: Django’s ORM enables efficient querying through lazy evaluation, ensuring that only the necessary data is fetched when needed. Additionally, the API can be optimized further with database indexing for fields used in queries, such as sorting or filtering criteria (e.g., date added, views, or other metadata).

3) Redis Caching:
Caching paginated results reduces the load on the database, particularly for frequently accessed pages. Redis, being an in-memory data store, provides extremely low-latency access to cached data, which significantly enhances the response time. The graceful fallback mechanism ensures that even if Redis is unavailable, the system continues to operate by serving data directly from the database.

4) Signals for Cache Invalidation:
By connecting Django signals (post_save, post_delete) to the Video model, cache invalidation happens automatically whenever there is a change to the video dataset (addition, update, or deletion). This ensures that no stale data is served, maintaining the integrity of the data in the cache.

5) Scalable API Design:
The API design considers future scalability with support for increasing numbers of video records and users. As the number of videos grows, the API remains responsive due to the combination of pagination and Redis caching. Redis can be horizontally scaled with clusters, allowing the caching layer to handle high-traffic loads.

### Additional Features
1) Custom Pagination Details:
The API returns additional pagination metadata (such as total_videos, total_pages, next_cursor) in the response. This provides clients with important information about the data and allows for easy navigation between pages. Such metadata is particularly useful in mobile apps or frontend interfaces for building smooth user experiences.

2) Error Handling and Graceful Degradation:
In case Redis is unavailable or encounters an error, the API handles this gracefully. The try-except blocks ensure that the absence of caching does not result in API failures. Instead, the system falls back on querying the database, maintaining uptime and a good user experience. Future enhancements could include monitoring for Redis availability and logging such events to alert developers of any issues, helping to maintain a stable production environment.

3) Security Considerations:
Django’s built-in security features such as CSRF protection, secure cookie handling, and SQL injection prevention are utilized to protect the API.
