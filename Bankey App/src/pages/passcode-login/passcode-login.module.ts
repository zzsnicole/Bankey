import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { PasscodeLoginPage } from './passcode-login';

@NgModule({
  declarations: [
    PasscodeLoginPage,
  ],
  imports: [
    IonicPageModule.forChild(PasscodeLoginPage),
  ],
})
export class PasscodeLoginPageModule {}
