import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { CallTellerPage } from './call-teller';

@NgModule({
  declarations: [
    CallTellerPage,
  ],
  imports: [
    IonicPageModule.forChild(CallTellerPage),
  ],
})
export class CallTellerPageModule {}
