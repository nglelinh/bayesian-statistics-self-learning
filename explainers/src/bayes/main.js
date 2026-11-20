import '../shared/ui.css';
import BayesRuleExplainer from './BayesRuleExplainer.svelte';
import ConjugateExplainer from './ConjugateExplainer.svelte';
import GridExplainer from './GridExplainer.svelte';
import McmcExplainer from './McmcExplainer.svelte';
import IntervalExplainer from './IntervalExplainer.svelte';
import CltExplainer from './CltExplainer.svelte';
import PpcExplainer from './PpcExplainer.svelte';
import RegressionExplainer from './RegressionExplainer.svelte';
import ShrinkExplainer from './ShrinkExplainer.svelte';
import IcExplainer from './IcExplainer.svelte';
import DecisionExplainer from './DecisionExplainer.svelte';
import GlmExplainer from './GlmExplainer.svelte';
import PoolingExplainer from './PoolingExplainer.svelte';
import ConfoundExplainer from './ConfoundExplainer.svelte';
import PvalueExplainer from './PvalueExplainer.svelte';
import LikelihoodExplainer from './LikelihoodExplainer.svelte';
import BfExplainer from './BfExplainer.svelte';
import CollinearExplainer from './CollinearExplainer.svelte';
import BiasVarExplainer from './BiasVarExplainer.svelte';
import HorseshoeExplainer from './HorseshoeExplainer.svelte';
import OverdispExplainer from './OverdispExplainer.svelte';
import GlmPpcExplainer from './GlmPpcExplainer.svelte';
import { mountAll, attr } from '../shared/mount.js';

// Ngôn ngữ: data-lang="vi|en" (mặc định lấy từ <html lang>). Bundle này chứa MỌI explainer của khóa học.
const lang = (el) => attr(el, 'lang', document.documentElement.lang === 'en' ? 'en' : 'vi');

// data-tab: tree|sequential   data-preset: disease|common|spam
mountAll('[data-demo="bayesrule-explainer"]', BayesRuleExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'tree'), preset: attr(el, 'preset', 'disease') }));
// data-tab: betabinom|gammapoisson|normalnormal   data-a, data-b (prior Beta: 1,1 | 2,2 | 10,10 | 8,2)   data-theta
mountAll('[data-demo="conjugate-explainer"]', ConjugateExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'betabinom'), a: attr(el, 'a', '1'), b: attr(el, 'b', '1'), theta: attr(el, 'theta', '0.7') }));
// data-prior: flat|beta22|beta55|tri|bimodal   data-k, data-n, data-points
mountAll('[data-demo="grid-explainer"]', GridExplainer, (el) => ({ lang: lang(el), prior: attr(el, 'prior', 'flat'), k: attr(el, 'k', '6'), n: attr(el, 'n', '9'), points: attr(el, 'points', '20') }));
// data-tab: metropolis|gibbs|hmc   data-target: beta|normal|bimodal
mountAll('[data-demo="mcmc-explainer"]', McmcExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'metropolis'), target: attr(el, 'target', 'beta') }));
mountAll('[data-demo="interval-explainer"]', IntervalExplainer, (el) => ({ lang: lang(el) }));
// data-tab: clt|lln   data-dist: uniform|exponential|bernoulli|bimodal
mountAll('[data-demo="clt-explainer"]', CltExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'clt'), dist: attr(el, 'dist', 'exponential') }));
// data-data: iid|streaky|alternating   data-stat: total|switches|longestRun
mountAll('[data-demo="ppc-explainer"]', PpcExplainer, (el) => ({ lang: lang(el), data: attr(el, 'data', 'streaky'), stat: attr(el, 'stat', 'switches') }));
// data-a, data-b: đường thật
mountAll('[data-demo="regression-explainer"]', RegressionExplainer, (el) => ({ lang: lang(el), a: attr(el, 'a', '1'), b: attr(el, 'b', '1.5') }));
// data-degree: 1–12
mountAll('[data-demo="shrink-explainer"]', ShrinkExplainer, (el) => ({ lang: lang(el), degree: attr(el, 'degree', '9') }));

// data-tab: waic|avg
mountAll('[data-demo="ic-explainer"]', IcExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'waic') }));
// data-tab: threshold|loss|voi
mountAll('[data-demo="decision-explainer"]', DecisionExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'threshold') }));
// data-tab: logistic|poisson
mountAll('[data-demo="glm-explainer"]', GlmExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'logistic') }));
// data-data: schools|equal
mountAll('[data-demo="pooling-explainer"]', PoolingExplainer, (el) => ({ lang: lang(el), data: attr(el, 'data', 'schools') }));
// data-tab: fork|collider|interaction
mountAll('[data-demo="confound-explainer"]', ConfoundExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'fork') }));
// data-tab: pnull|tdist|power
mountAll('[data-demo="pvalue-explainer"]', PvalueExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'pnull') }));
// data-tab: binom|poisson|predictive
mountAll('[data-demo="likelihood-explainer"]', LikelihoodExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'binom') }));

// data-tab: seq|prior
mountAll('[data-demo="bf-explainer"]', BfExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'seq') }));
mountAll('[data-demo="collinear-explainer"]', CollinearExplainer, (el) => ({ lang: lang(el) }));
// data-tau: 100|3|0.5
mountAll('[data-demo="biasvar-explainer"]', BiasVarExplainer, (el) => ({ lang: lang(el), tau: attr(el, 'tau', '3') }));
mountAll('[data-demo="horseshoe-explainer"]', HorseshoeExplainer, (el) => ({ lang: lang(el) }));
// data-data: nb|poisson
mountAll('[data-demo="overdisp-explainer"]', OverdispExplainer, (el) => ({ lang: lang(el), data: attr(el, 'data', 'nb') }));
// data-tab: logistic|poisson
mountAll('[data-demo="glmppc-explainer"]', GlmPpcExplainer, (el) => ({ lang: lang(el), tab: attr(el, 'tab', 'logistic') }));
