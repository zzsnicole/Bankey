import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { KeyProfilePage } from './key-profile';

@NgModule({
  declarations: [
    KeyProfilePage,
  ],
  imports: [
    IonicPageModule.forChild(KeyProfilePage),
  ],
})
export class KeyProfilePageModule {}
