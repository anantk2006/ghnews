module.exports = {
    apps: [
      {
        name: 'react-frontend',
        script: 'npx',
        args: 'serve -s frontend/build -p 80',
        watch: false,
        instances: 1,
      },
      {
        name: 'fastapi-backend',
        script: 'gunicorn',
        args: 'backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000',
        watch: false,
        instances: 1,
      },
    ],
  };