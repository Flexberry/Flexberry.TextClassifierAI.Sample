import $ from 'jquery';
import EmberFlexberryTranslations from 'ember-flexberry/locales/en/translations';

import IISReportsTextClassifierAiReportLForm from './forms/i-i-s-reports-text-classifier-ai-report-l';
import IISReportsTextClassifierAiReportTypeLForm from './forms/i-i-s-reports-text-classifier-ai-report-type-l';
import IISReportsTextClassifierAiReportEForm from './forms/i-i-s-reports-text-classifier-ai-report-e';
import IISReportsTextClassifierAiReportTypeEForm from './forms/i-i-s-reports-text-classifier-ai-report-type-e';
import IISReportsTextClassifierAiReportTypeModel from './models/i-i-s-reports-text-classifier-ai-report-type';
import IISReportsTextClassifierAiReportModel from './models/i-i-s-reports-text-classifier-ai-report';

const translations = {};
$.extend(true, translations, EmberFlexberryTranslations);

$.extend(true, translations, {
  models: {
    'i-i-s-reports-text-classifier-ai-report-type': IISReportsTextClassifierAiReportTypeModel,
    'i-i-s-reports-text-classifier-ai-report': IISReportsTextClassifierAiReportModel
  },

  'application-name': 'Reports ocr and search',

  forms: {
    loading: {
      'spinner-caption': 'Loading stuff, please wait for a moment...'
    },
    index: {
      greeting: 'Welcome to ember-flexberry test stand!'
    },

    application: {
      header: {
        menu: {
          'sitemap-button': {
            title: 'Menu'
          },
          'user-settings-service-checkbox': {
            caption: 'Use service to save user settings'
          },
          'show-menu': {
            caption: 'Show menu'
          },
          'hide-menu': {
            caption: 'Hide menu'
          },
          'language-dropdown': {
            caption: 'Application language',
            placeholder: 'Choose language'
          }
        },
        login: {
          caption: 'Login'
        },
        logout: {
          caption: 'Logout'
        }
      },

      footer: {
        'application-name': 'Reports ocr and search',
        'application-version': {
          caption: 'Addon version {{version}}',
          title: 'It is version of ember-flexberry addon, which uses in this dummy application ' +
          '(npm version + commit sha). ' +
          'Click to open commit on GitHub.'
        }
      },

      sitemap: {
        'application-name': {
          caption: 'Reports ocr and search',
          title: 'Reports ocr and search'
        },
        'application-version': {
          caption: 'Addon version {{version}}',
          title: 'It is version of ember-flexberry addon, which uses in this dummy application ' +
          '(npm version + commit sha). ' +
          'Click to open commit on GitHub.'
        },
        index: {
          caption: 'Home',
          title: ''
        },
        'reports-text-classifier-ai': {
          caption: 'ReportsTextClassifierAi',
          title: 'ReportsTextClassifierAi',
          'i-i-s-reports-text-classifier-ai-report-l': {
            caption: 'ReportL',
            title: 'Report'
          },
          'i-i-s-reports-text-classifier-ai-report-type-l': {
            caption: 'ReportTypeL',
            title: ''
          }
        }
      }
    },

    'edit-form': {
      'save-success-message-caption': 'Save operation succeed',
      'save-success-message': 'Object saved',
      'save-error-message-caption': 'Save operation failed',
      'delete-success-message-caption': 'Delete operation succeed',
      'delete-success-message': 'Object deleted',
      'delete-error-message-caption': 'Delete operation failed'
    },
    'i-i-s-reports-text-classifier-ai-report-l': IISReportsTextClassifierAiReportLForm,
    'i-i-s-reports-text-classifier-ai-report-type-l': IISReportsTextClassifierAiReportTypeLForm,
    'i-i-s-reports-text-classifier-ai-report-e': IISReportsTextClassifierAiReportEForm,
    'i-i-s-reports-text-classifier-ai-report-type-e': IISReportsTextClassifierAiReportTypeEForm
  },

});

export default translations;
