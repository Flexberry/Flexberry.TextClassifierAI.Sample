import $ from 'jquery';
import EmberFlexberryTranslations from 'ember-flexberry/locales/ru/translations';

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
      'spinner-caption': 'Данные загружаются, пожалуйста подождите...'
    },
    index: {
      greeting: 'Добро пожаловать на тестовый стенд ember-flexberry!'
    },

    application: {
      header: {
        menu: {
          'sitemap-button': {
            title: 'Меню'
          },
          'user-settings-service-checkbox': {
            caption: 'Использовать сервис сохранения пользовательских настроек'
          },
          'show-menu': {
            caption: 'Показать меню'
          },
          'hide-menu': {
            caption: 'Скрыть меню'
          },
          'language-dropdown': {
            caption: 'Язык приложения',
            placeholder: 'Выберите язык'
          }
        },
        login: {
          caption: 'Вход'
        },
        logout: {
          caption: 'Выход'
        }
      },

      footer: {
        'application-name': 'Reports ocr and search',
        'application-version': {
          caption: 'Версия аддона {{version}}',
          title: 'Это версия аддона ember-flexberry, которая сейчас используется в этом тестовом приложении ' +
          '(версия npm-пакета + хэш коммита). ' +
          'Кликните, чтобы перейти на GitHub.'
        }
      },

      sitemap: {
        'application-name': {
          caption: 'Reports ocr and search',
          title: 'Reports ocr and search'
        },
        'application-version': {
          caption: 'Версия аддона {{version}}',
          title: 'Это версия аддона ember-flexberry, которая сейчас используется в этом тестовом приложении ' +
          '(версия npm-пакета + хэш коммита). ' +
          'Кликните, чтобы перейти на GitHub.'
        },
        index: {
          caption: 'Главная',
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
      'save-success-message-caption': 'Сохранение завершилось успешно',
      'save-success-message': 'Объект сохранен',
      'save-error-message-caption': 'Ошибка сохранения',
      'delete-success-message-caption': 'Удаление завершилось успешно',
      'delete-success-message': 'Объект удален',
      'delete-error-message-caption': 'Ошибка удаления'
    },
    'i-i-s-reports-text-classifier-ai-report-l': IISReportsTextClassifierAiReportLForm,
    'i-i-s-reports-text-classifier-ai-report-type-l': IISReportsTextClassifierAiReportTypeLForm,
    'i-i-s-reports-text-classifier-ai-report-e': IISReportsTextClassifierAiReportEForm,
    'i-i-s-reports-text-classifier-ai-report-type-e': IISReportsTextClassifierAiReportTypeEForm
  },

});

export default translations;
