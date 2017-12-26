import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PersonalDetailAddressKeyPage } from './personal-detail-address-key';

@NgModule({
  declarations: [
    PersonalDetailAddressKeyPage,
  ],
  imports: [
    IonicPageModule.forChild(PersonalDetailAddressKeyPage),
  ],
})
export class PersonalDetailAddressKeyPageModule {}
