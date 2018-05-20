// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  firebase : {
	  apiKey: "AIzaSyAOGDk9lU3d_-e8HgTatwEq7xsgfL4iXHU",
	  authDomain: "angular-5-with-firebase.firebaseapp.com",
    databaseURL: "https://angular-5-with-firebase.firebaseio.com",
    projectId: "angular-5-with-firebase",
    storageBucket: "angular-5-with-firebase.appspot.com",
    messagingSenderId: "787763943684"
  }
};
