import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ProvidentiaHomeModule } from './home';
import { ProvidentiaNewJobModule } from './job';
import { ProvidentiaDatabasesModule } from './databases';
import { ProvidentiaHistoryModule } from './history';
import { ProvidentiaBenchmarkModule } from './benchmark';
import { ProvidentiaClassifierModule } from './classifier';
import { ProvidentiaPerformanceModule } from './performance';
import { AngularMaterialModule } from './material.module';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { ProvidentiaAppRoutingModule } from './app-routing.module';

import { NavbarComponent, FooterComponent, ErrorComponent, SidenavbarComponent } from './layouts';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ErrorComponent,
    FooterComponent,
    SidenavbarComponent,
  ],
  imports: [
    AngularMaterialModule,
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    ProvidentiaHomeModule,
    ProvidentiaNewJobModule,
    ProvidentiaDatabasesModule,
    ProvidentiaHistoryModule,
    ProvidentiaBenchmarkModule,
    ProvidentiaClassifierModule,
    ProvidentiaPerformanceModule,
    ProvidentiaAppRoutingModule,
    MDBBootstrapModule.forRoot()
  ],
  bootstrap: [AppComponent]
})
export class ProvidentiaAppModule { }
