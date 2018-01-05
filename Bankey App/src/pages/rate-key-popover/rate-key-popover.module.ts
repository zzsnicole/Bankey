import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { RateKeyPopoverPage } from './rate-key-popover';

@NgModule({
  declarations: [
    RateKeyPopoverPage,
  ],
  imports: [
    IonicPageModule.forChild(RateKeyPopoverPage),
  ],
})
export class RateKeyPopoverPageModule {}
