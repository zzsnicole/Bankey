import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { KeyRequestConfirmPage } from './key-request-confirm';

@NgModule({
  declarations: [
    KeyRequestConfirmPage,
  ],
  imports: [
    IonicPageModule.forChild(KeyRequestConfirmPage),
  ],
})
export class KeyRequestConfirmPageModule {}
