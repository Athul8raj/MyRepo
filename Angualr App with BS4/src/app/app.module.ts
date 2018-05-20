import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AngularFireModule } from 'angularfire2';
import { AngularFireDatabaseModule } from 'angularfire2/database';
import { AngularFireAuthModule } from 'angularfire2/auth';
import { AppComponent } from './app.component';
import { environment } from './../environments/environment';
import { AppNavbarComponent } from './app-navbar/app-navbar.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CoursesListComponent } from './courses-list/courses-list.component';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';





const appRoutes:Routes = [
{path: 'login', component : LoginComponent},
{path: 'courses', component : CoursesListComponent}]

@NgModule({
  declarations: [
    AppComponent,
    AppNavbarComponent,
    CoursesListComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
	AngularFireAuthModule,
	AngularFireModule.initializeApp(environment.firebase),
	AngularFireDatabaseModule, 
	NgbModule.forRoot(),
	RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
