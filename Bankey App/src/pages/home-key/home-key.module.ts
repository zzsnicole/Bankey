import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { HomeKeyPage } from './home-key';

@NgModule({
  declarations: [
    HomeKeyPage,
  ],
  imports: [
    IonicPageModule.forChild(HomeKeyPage),
  ],
})
export class HomeKeyPageModule {}
