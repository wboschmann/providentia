import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ProvidentiaHomeModule } from './home';
import { ProvidentiaNewJobModule } from './job';
import { ProvidentiaAboutModule } from './about';
import { ProvidentiaHistoryModule } from './history';
import { AngularMaterialModule } from './material.module';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { ProvidentiaAppRoutingModule } from './app-routing.module';

import { D3Service, D3_DIRECTIVES } from './d3';

import { GraphComponent } from './visuals/graph/graph.component';
import { SHARED_VISUALS } from './visuals/shared';

import { NavbarComponent, FooterComponent, ErrorComponent, SidenavbarComponent } from './layouts';

@NgModule({
  declarations: [
    AppComponent,
    GraphComponent,
    ...SHARED_VISUALS,
    ...D3_DIRECTIVES,
    NavbarComponent,
    ErrorComponent,
    FooterComponent,
    SidenavbarComponent,
  ],
  imports: [
    AngularMaterialModule,
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpModule,
    HttpClientModule,
    ProvidentiaHomeModule,
    ProvidentiaNewJobModule,
    ProvidentiaAboutModule,
    ProvidentiaHistoryModule,
    ProvidentiaAppRoutingModule,
    MDBBootstrapModule.forRoot()
  ],
  providers: [
    D3Service
  ],
  bootstrap: [AppComponent]
})
export class ProvidentiaAppModule { }