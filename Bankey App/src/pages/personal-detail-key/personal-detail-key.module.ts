import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PersonalDetailKeyPage } from './personal-detail-key';

@NgModule({
  declarations: [
    PersonalDetailKeyPage,
  ],
  imports: [
    IonicPageModule.forChild(PersonalDetailKeyPage),
  ],
})
export class PersonalDetailKeyPageModule {}
