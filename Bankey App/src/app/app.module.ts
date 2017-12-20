import {InviteFriendsPage} from './../pages/invite-friends/invite-friends';
import {PersonalDetailsPage} from './../pages/personal-details/personal-details';
import {EnterOtpPage} from './../pages/enter-otp/enter-otp';
import {CreatePasswordPage} from './../pages/create-password/create-password';
import {BrowserModule} from '@angular/platform-browser';
import {ErrorHandler, NgModule} from '@angular/core';
import {IonicApp, IonicErrorHandler, IonicModule} from 'ionic-angular';
import {SplashScreen} from '@ionic-native/splash-screen';
import {StatusBar} from '@ionic-native/status-bar';
import {TypeaheadModule} from 'ngx-bootstrap';
import {NgxIntlTelInputModule} from 'ngx-intl-tel-input';

import {BankeyApp} from './app.component';
import {HomePage} from '../pages/home/home';
import {MobilePage} from '../pages/mobile/mobile';
import {Camera} from '@ionic-native/camera';
import {SocialSharing} from '@ionic-native/social-sharing';
import {SignInPage} from "../pages/sign-in/sign-in";
import {SignUpPage} from "../pages/sign-up/sign-up";
import { HttpClientProvider } from '../providers/http-client/http-client';

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
        InviteFriendsPage
    ],
    imports: [
        BrowserModule,
        NgxIntlTelInputModule,
        TypeaheadModule.forRoot(),
        IonicModule.forRoot(BankeyApp)
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
        InviteFriendsPage
    ],
    providers: [
        StatusBar,
        SplashScreen,
        Camera,
        SocialSharing,
        {provide: ErrorHandler, useClass: IonicErrorHandler},
    HttpClientProvider
    ]
})
export class AppModule {
}
