import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType
});

Router.map(function () {
  this.route('i-i-s-reports-text-classifier-ai-report-l');
  this.route('i-i-s-reports-text-classifier-ai-report-e',
  { path: 'i-i-s-reports-text-classifier-ai-report-e/:id' });
  this.route('i-i-s-reports-text-classifier-ai-report-e.new',
  { path: 'i-i-s-reports-text-classifier-ai-report-e/new' });
  this.route('i-i-s-reports-text-classifier-ai-report-type-l');
  this.route('i-i-s-reports-text-classifier-ai-report-type-e',
  { path: 'i-i-s-reports-text-classifier-ai-report-type-e/:id' });
  this.route('i-i-s-reports-text-classifier-ai-report-type-e.new',
  { path: 'i-i-s-reports-text-classifier-ai-report-type-e/new' });
});

export default Router;
