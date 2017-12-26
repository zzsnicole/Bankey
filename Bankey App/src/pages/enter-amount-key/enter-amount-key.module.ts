import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EnterAmountKeyPage } from './enter-amount-key';

@NgModule({
  declarations: [
    EnterAmountKeyPage,
  ],
  imports: [
    IonicPageModule.forChild(EnterAmountKeyPage),
  ],
})
export class EnterAmountKeyPageModule {}
