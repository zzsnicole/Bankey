import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EnterAmountPage } from './enter-amount';

@NgModule({
  declarations: [
    EnterAmountPage,
  ],
  imports: [
    IonicPageModule.forChild(EnterAmountPage),
  ],
})
export class EnterAmountPageModule {}
