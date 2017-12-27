import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ConfirmationCodePage } from './confirmation-code';

@NgModule({
  declarations: [
    ConfirmationCodePage,
  ],
  imports: [
    IonicPageModule.forChild(ConfirmationCodePage),
  ],
})
export class ConfirmationCodePageModule {}
