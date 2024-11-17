module.exports = {
    apps: [
      {
        name: 'react-frontend',
        script: 'npm',
        args: 'start',
        watch: false,
        instances: 1,
      },
    //   {
    //     name: 'fastapi-backend',
    //     script: 'hypercorn',
    //     args: 'backend.main:app',
    //     watch: false,
    //     instances: 1,
    //   },
    ],
  };