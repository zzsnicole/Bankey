import {InviteFriendsPage} from '../pages/invite-friends/invite-friends';
import {PersonalDetailsPage} from '../pages/personal-details/personal-details';
import {EnterOtpPage} from '../pages/enter-otp/enter-otp';
import {CreatePasswordPage} from '../pages/create-password/create-password';
import {BrowserModule} from '@angular/platform-browser';
import {ErrorHandler, NgModule} from '@angular/core';
import {IonicApp, IonicErrorHandler, IonicModule} from 'ionic-angular';
import {SplashScreen} from '@ionic-native/splash-screen';
import {StatusBar} from '@ionic-native/status-bar';
import {GoogleMaps} from '@ionic-native/google-maps';
import { File } from '@ionic-native/file';

import {BankeyApp} from './app.component';
import {HomePage} from '../pages/home/home';
import {MobilePage} from '../pages/mobile/mobile';
import {Camera} from '@ionic-native/camera';
import {SocialSharing} from '@ionic-native/social-sharing';
import {SignInPage} from "../pages/sign-in/sign-in";
import {SignUpPage} from "../pages/sign-up/sign-up";
import {HttpClientModule } from '@angular/common/http';
import {HttpClientProvider} from "../providers/http-client/http-client";
import {CallTellerPage} from "../pages/call-teller/call-teller";
import {HomeKeyPage} from "../pages/home-key/home-key";
import {EnterAmountKeyPage} from "../pages/enter-amount-key/enter-amount-key";
import {PersonalDetailKeyPage} from "../pages/personal-detail-key/personal-detail-key";
import {PersonalDetailAddressKeyPage} from "../pages/personal-detail-address-key/personal-detail-address-key";
import {PersonalDetailEmailKeyPage} from "../pages/personal-detail-email-key/personal-detail-email-key";
import {InviteFriendsKeyPage} from "../pages/invite-friends-key/invite-friends-key";
import {PasscodeLoginPage} from "../pages/passcode-login/passcode-login";
import {EnterAmountPage} from "../pages/enter-amount/enter-amount";
import {SelectKeyPage} from "../pages/select-key/select-key";
import {KeyRequestConfirmPage} from "../pages/key-request-confirm/key-request-confirm";
import {ConfirmationCodePage} from "../pages/confirmation-code/confirmation-code";
import {MyAccountPage} from "../pages/my-account/my-account";
import {KeyProfilePage} from "../pages/key-profile/key-profile";
import { SelectSearchableModule } from '../components/select-searchable/select-searchable-module';
import { CommonFunctionsProvider } from '../providers/common-functions/common-functions';
import {PendingRequestPage} from "../pages/pending-request/pending-request";
import {TransactionReferencePage} from "../pages/transaction-reference/transaction-reference";
import { Ionic2RatingModule } from 'ionic2-rating';

@NgModule({
    declarations: [
        BankeyApp,
        HomePage,
        SignInPage,
        SignUpPage,
        MobilePage,
        CreatePasswordPage,
        EnterOtpPage,
        PersonalDetailsPage,
        InviteFriendsPage,
        CallTellerPage,
        HomeKeyPage,
        EnterAmountKeyPage,
        PersonalDetailKeyPage,
        PersonalDetailAddressKeyPage,
        PersonalDetailEmailKeyPage,
        InviteFriendsKeyPage,
        PasscodeLoginPage,
        EnterAmountPage,
        SelectKeyPage,
        KeyRequestConfirmPage,
        ConfirmationCodePage,
        MyAccountPage,
        KeyProfilePage,
        PendingRequestPage,
        TransactionReferencePage
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        IonicModule.forRoot(BankeyApp),
        SelectSearchableModule,
        Ionic2RatingModule
    ],
    bootstrap: [IonicApp],
    entryComponents: [
        BankeyApp,
        HomePage,
        SignInPage,
        SignUpPage,
        MobilePage,
        CreatePasswordPage,
        EnterOtpPage,
        PersonalDetailsPage,
        InviteFriendsPage,
        CallTellerPage,
        HomeKeyPage,
        EnterAmountKeyPage,
        PersonalDetailKeyPage,
        PersonalDetailAddressKeyPage,
        PersonalDetailEmailKeyPage,
        InviteFriendsKeyPage,
        PasscodeLoginPage,
        EnterAmountPage,
        SelectKeyPage,
        KeyRequestConfirmPage,
        ConfirmationCodePage,
        MyAccountPage,
        KeyProfilePage,
        PendingRequestPage,
        TransactionReferencePage
    ],
    providers: [
        StatusBar,
        SplashScreen,
        Camera,
        SocialSharing,
        GoogleMaps,
        File,
        {provide: ErrorHandler, useClass: IonicErrorHandler},
        HttpClientProvider,
        CommonFunctionsProvider
    ]
})
export class AppModule {
}
