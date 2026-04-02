# NeuraBay Backend

Production-ready FastAPI backend for NeuraBay.

## Structure

/app
  /api
    /v1
      endpoints/
        auth.py
        users.py
        services.py
        blog.py
        contact.py
        career.py
        testimonials.py
  /core
    config.py
    security.py
    dependencies.py
    logging.py
  /models
    base.py
    user.py
    service.py
    blog.py
    category.py
    tag.py
    job.py
    application.py
    contact.py
    testimonial.py
    blog_tag.py
  /schemas
    user.py
    service.py
    blog.py
    category.py
    tag.py
    job.py
    application.py
    contact.py
    testimonial.py
  /crud
    user.py
    service.py
    blog.py
    category.py
    tag.py
    job.py
    application.py
    contact.py
    testimonial.py
  /services
    auth_service.py
    user_service.py
    service_service.py
    blog_service.py
    job_service.py
    contact_service.py
    testimonial_service.py
    ai_service.py
  /db
    base.py
    session.py
    init_db.py
  /utils
    email.py
    helpers.py

main.py

## Example Responses

Login response:
```
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer"
}
```

Standard API response:
```
{
  "success": true,
  "data": {"id": 1, "title": "AI Consulting"}
}
```
