module.exports = {
    apps: [
      {
        name: 'react-frontend',
        script: 'npm',
        args: 'start',
        watch: false,
        instances: 1,
      },
      {
        name: 'fastapi-backend',
        script: 'gunicorn',
        args: '-w 1 -k uvicorn.workers.UvicornWorker backend.main:app', 
        watch: false,
        instances: 1,
      },
    ],
  };