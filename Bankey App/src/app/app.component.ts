import { Component } from '@angular/core';
import {Platform, Select} from 'ionic-angular';
import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';

import { HomePage } from '../pages/home/home';
import {PasscodeLoginPage} from "../pages/passcode-login/passcode-login";
import {CreatePasswordPage} from "../pages/create-password/create-password";
import {PersonalDetailEmailKeyPage} from "../pages/personal-detail-email-key/personal-detail-email-key";
import {PersonalDetailsPage} from "../pages/personal-details/personal-details";
import {InviteFriendsPage} from "../pages/invite-friends/invite-friends";
import {EnterAmountPage} from "../pages/enter-amount/enter-amount";
import {KeyProfilePage} from "../pages/key-profile/key-profile";
import {ConfirmationCodePage} from "../pages/confirmation-code/confirmation-code";
import {EnterOtpPage} from "../pages/enter-otp/enter-otp";
import {TransactionReferencePage} from "../pages/transaction-reference/transaction-reference"
import {SelectKeyPage} from "../pages/select-key/select-key";
import {MyAccountPage} from "../pages/my-account/my-account";
import {HomeKeyPage} from "../pages/home-key/home-key";
import {SetServiceFeePage} from "../pages/set-service-fee/set-service-fee";
import {InviteFriendsKeyPage} from "../pages/invite-friends-key/invite-friends-key";

@Component({
  templateUrl: 'app.html'
})
export class BankeyApp {
  rootPage:any = InviteFriendsKeyPage;

  constructor(platform: Platform, statusBar: StatusBar, splashScreen: SplashScreen) {
    platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      statusBar.styleDefault();
      splashScreen.hide();
    });
  }
}
