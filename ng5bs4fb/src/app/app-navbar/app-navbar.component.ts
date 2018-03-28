import { Component, OnInit } from '@angular/core';
import { AngularFireAuthModule, AngularFireAuth } from 'angularfire2/auth';
import * as firebase from 'firebase/app';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-navbar',
  templateUrl: './app-navbar.component.html',
  styleUrls: ['./app-navbar.component.css']
})
export class AppNavbarComponent implements OnInit {
	user: Observable<firebase.User>;
	authenticated : boolean = false;

  constructor(public af: AngularFireAuth) { 
	this.af.authState.subscribe
	{(auth) =>{
		if(auth!= null)
		{
			this.user = af.authState;
			this.authenticated = true;
		}
	}
		}
  }

  ngOnInit() {
  }

  loginGoogle(){
	  this.af.auth.signInWithPopup(new firebase.auth.GoogleAuthProvider());
	  this.authenticated= true;
  }
  loginFb(){
	  this.af.auth.signInWithPopup(new firebase.auth.FacebookAuthProvider());
	  this.authenticated= true;
  }
  
  logout(){
	  this.af.auth.signOut();
	  this.authenticated = false;
  }
}
