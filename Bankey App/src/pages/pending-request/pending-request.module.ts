import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PendingRequestPage } from './pending-request';

@NgModule({
  declarations: [
    PendingRequestPage,
  ],
  imports: [
    IonicPageModule.forChild(PendingRequestPage),
  ],
})
export class PendingRequestPageModule {}
