import Controller from '@ember/controller';
import { computed } from '@ember/object';

export default Controller.extend({
  sitemap: computed('i18n.locale', function () {
    let i18n = this.get('i18n');

    return {
      nodes: [
        {
          link: 'index',
          icon: 'home',
          caption: i18n.t('forms.application.sitemap.index.caption'),
          title: i18n.t('forms.application.sitemap.index.title'),
          children: null
        }, {
          link: null,
          icon: 'list',
          caption: i18n.t('forms.application.sitemap.reports-text-classifier-ai.caption'),
          title: i18n.t('forms.application.sitemap.reports-text-classifier-ai.title'),
          children: [{
            link: 'i-i-s-reports-text-classifier-ai-report-l',
            caption: i18n.t('forms.application.sitemap.reports-text-classifier-ai.i-i-s-reports-text-classifier-ai-report-l.caption'),
            title: i18n.t('forms.application.sitemap.reports-text-classifier-ai.i-i-s-reports-text-classifier-ai-report-l.title'),
            icon: 'book',
            children: null
          }, {
            link: 'i-i-s-reports-text-classifier-ai-report-type-l',
            caption: i18n.t('forms.application.sitemap.reports-text-classifier-ai.i-i-s-reports-text-classifier-ai-report-type-l.caption'),
            title: i18n.t('forms.application.sitemap.reports-text-classifier-ai.i-i-s-reports-text-classifier-ai-report-type-l.title'),
            icon: 'list',
            children: null
          }]
        }
      ]
    };
  }),
})