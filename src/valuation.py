"""
ارزش‌گذاری شرکت‌ها با روش‌های مختلف و پیشرفته
مناسب برای بازار سرمایه ایران

مفروضات کلیدی بازار ایران:
- نرخ تورم: 30-50% سالانه
- نرخ بهره بدون ریسک (اوراق): 18-25%
- صرف ریسک بازار (ERP): 8-12%
- نرخ رشد بلندمدت GDP: 3-5%
- نرخ مالیات شرکتی: 25%
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class CompanyValuation:
    """کلاس ارزش‌گذاری شرکت"""
    
    def __init__(self, company_name: str, financial_data: Dict[str, pd.DataFrame]):
        self.company_name = company_name
        self.data = financial_data
        self.valuation_results = {}
        
        # مفروضات بازار ایران
        self.iran_assumptions = {
            'risk_free_rate': 0.22,  # نرخ بهره بدون ریسک (اوراق خزانه)
            'market_risk_premium': 0.10,  # صرف ریسک بازار
            'inflation_rate': 0.40,  # نرخ تورم میانگین
            'terminal_growth_max': 0.10,  # حداکثر رشد پایدار
            'corporate_tax_rate': 0.25,  # نرخ مالیات شرکتی
            'gdp_growth': 0.04,  # رشد GDP بلندمدت
        }
    
    def calculate_wacc(self, equity_value: float, debt_value: float, 
                       cost_of_equity: float, cost_of_debt: float) -> Dict[str, float]:
        """
        محاسبه میانگین موزون هزینه سرمایه (WACC)
        
        مفروضات:
        - نرخ مالیات: 25% (قانون مالیات‌های مستقیم ایران)
        - ساختار سرمایه بر اساس ارزش بازار
        
        WACC = (E/V × Re) + (D/V × Rd × (1 - Tc))
        """
        total_value = equity_value + debt_value
        
        if total_value == 0:
            return {'wacc': cost_of_equity, 'weight_equity': 1.0, 'weight_debt': 0.0}
        
        weight_equity = equity_value / total_value
        weight_debt = debt_value / total_value
        
        # هزینه بدهی پس از مالیات
        after_tax_cost_debt = cost_of_debt * (1 - self.iran_assumptions['corporate_tax_rate'])
        
        wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_cost_debt)
        
        return {
            'wacc': wacc,
            'weight_equity': weight_equity,
            'weight_debt': weight_debt,
            'cost_of_equity': cost_of_equity,
            'cost_of_debt': cost_of_debt,
            'after_tax_cost_debt': after_tax_cost_debt
        }
    
    def calculate_cost_of_equity_capm(self, beta: float = 1.0) -> Dict[str, float]:
        """
        محاسبه هزینه حقوق صاحبان سهام با مدل CAPM
        
        مفروضات بازار ایران:
        - نرخ بدون ریسک: 22% (اوراق خزانه اسلامی)
        - صرف ریسک بازار: 10% (میانگین تاریخی)
        - بتا: بر اساس نوسانات نسبت به شاخص کل
        
        Re = Rf + β(Rm - Rf)
        """
        rf = self.iran_assumptions['risk_free_rate']
        erp = self.iran_assumptions['market_risk_premium']
        
        cost_of_equity = rf + (beta * erp)
        
        return {
            'cost_of_equity': cost_of_equity,
            'risk_free_rate': rf,
            'beta': beta,
            'market_risk_premium': erp,
            'explanation': f'Re = {rf:.1%} + {beta:.2f} × {erp:.1%} = {cost_of_equity:.1%}'
        }
    
    def dcf_valuation(self, 
                      free_cash_flow: float,
                      growth_rate: float,
                      discount_rate: float,
                      terminal_growth: float,
                      projection_years: int = 5,
                      detailed: bool = True) -> Dict[str, any]:
        """
        ارزش‌گذاری با روش جریان نقدی آزاد تنزیل شده (DCF)
        
        مفروضات:
        -----------
        - افق زمانی: 5 سال (استاندارد بازار ایران)
        - نرخ تنزیل: WACC (8-25% بسته به ریسک)
        - نرخ رشد پایدار: حداکثر 10% (محدودیت بازار ایران)
        - جریان نقدی: FCF = EBIT(1-T) + DA - CapEx - ΔWC
        
        Parameters:
        -----------
        free_cash_flow: جریان نقدی آزاد سال جاری (میلیون ریال)
        growth_rate: نرخ رشد پیش‌بینی دوره صریح (%)
        discount_rate: نرخ تنزیل WACC (%)
        terminal_growth: نرخ رشد پایدار (%) - حداکثر رشد GDP
        projection_years: تعداد سال‌های پیش‌بینی
        """
        
        try:
            # محدودیت نرخ رشد پایدار
            if terminal_growth > self.iran_assumptions['terminal_growth_max']:
                terminal_growth = self.iran_assumptions['terminal_growth_max']
                print(f"⚠️ نرخ رشد پایدار به {terminal_growth:.1%} محدود شد")
            
            # محاسبه جریان‌های نقدی پیش‌بینی شده
            projected_fcf = []
            projected_fcf_nominal = []
            
            for year in range(1, projection_years + 1):
                # FCF اسمی
                fcf_nominal = free_cash_flow * ((1 + growth_rate) ** year)
                projected_fcf_nominal.append(fcf_nominal)
                
                # FCF تنزیل شده
                pv_fcf = fcf_nominal / ((1 + discount_rate) ** year)
                projected_fcf.append(pv_fcf)
            
            pv_projected_fcf = sum(projected_fcf)
            
            # محاسبه ارزش پایانی (Terminal Value) با روش Gordon Growth
            # TV = FCF(n+1) / (WACC - g)
            last_year_fcf = projected_fcf_nominal[-1]
            terminal_fcf = last_year_fcf * (1 + terminal_growth)
            
            if discount_rate <= terminal_growth:
                print(f"⚠️ نرخ تنزیل ({discount_rate:.1%}) باید بیشتر از رشد پایدار ({terminal_growth:.1%}) باشد")
                terminal_growth = discount_rate - 0.02  # کاهش 2%
            
            terminal_value = terminal_fcf / (discount_rate - terminal_growth)
            pv_terminal_value = terminal_value / ((1 + discount_rate) ** projection_years)
            
            # ارزش کل شرکت (Enterprise Value)
            enterprise_value = pv_projected_fcf + pv_terminal_value
            
            # درصد ارزش پایانی از کل
            terminal_percent = (pv_terminal_value / enterprise_value) * 100 if enterprise_value > 0 else 0
            
            result = {
                'enterprise_value': enterprise_value,
                'pv_projected_fcf': pv_projected_fcf,
                'pv_terminal_value': pv_terminal_value,
                'terminal_value': terminal_value,
                'terminal_percent': terminal_percent,
                'projected_fcf_pv': projected_fcf,
                'projected_fcf_nominal': projected_fcf_nominal,
                'assumptions': {
                    'fcf_base': free_cash_flow,
                    'growth_rate': growth_rate,
                    'discount_rate': discount_rate,
                    'terminal_growth': terminal_growth,
                    'projection_years': projection_years
                },
                'sensitivity': self._dcf_sensitivity_analysis(
                    free_cash_flow, growth_rate, discount_rate, terminal_growth
                ) if detailed else {}
            }
            
            return result
            
        except Exception as e:
            print(f"خطا در محاسبه DCF: {e}")
            return {}
    
    def _dcf_sensitivity_analysis(self, fcf, growth, wacc, terminal_growth):
        """تحلیل حساسیت DCF نسبت به تغییرات WACC و نرخ رشد"""
        wacc_range = [wacc - 0.02, wacc, wacc + 0.02]
        growth_range = [growth - 0.02, growth, growth + 0.02]
        
        sensitivity_matrix = []
        for w in wacc_range:
            row = []
            for g in growth_range:
                if w > terminal_growth:
                    result = self.dcf_valuation(fcf, g, w, terminal_growth, 5, False)
                    row.append(result.get('enterprise_value', 0))
                else:
                    row.append(0)
            sensitivity_matrix.append(row)
        
        return {
            'wacc_range': wacc_range,
            'growth_range': growth_range,
            'values': sensitivity_matrix
        }
    
    def pe_valuation(self, 
                     earnings: float,
                     industry_pe: float,
                     growth_adjustment: float = 1.0) -> Dict[str, float]:
        """
        ارزش‌گذاری با روش P/E
        
        Parameters:
        -----------
        earnings: سود خالص سال جاری
        industry_pe: میانگین P/E صنعت
        growth_adjustment: ضریب تعدیل رشد
        """
        
        try:
            adjusted_pe = industry_pe * growth_adjustment
            equity_value = earnings * adjusted_pe
            
            return {
                'equity_value': equity_value,
                'implied_pe': adjusted_pe,
                'earnings': earnings
            }
            
        except Exception as e:
            print(f"خطا در محاسبه P/E: {e}")
            return {}
    
    def pb_valuation(self,
                     book_value: float,
                     roe: float,
                     required_return: float) -> Dict[str, float]:
        """
        ارزش‌گذاری با روش P/B
        
        Parameters:
        -----------
        book_value: ارزش دفتری
        roe: بازده حقوق صاحبان سهام
        required_return: بازده مورد انتظار
        """
        
        try:
            # P/B = ROE / Required Return
            pb_ratio = roe / required_return if required_return > 0 else 1.0
            equity_value = book_value * pb_ratio
            
            return {
                'equity_value': equity_value,
                'implied_pb': pb_ratio,
                'book_value': book_value
            }
            
        except Exception as e:
            print(f"خطا در محاسبه P/B: {e}")
            return {}
    
    def ev_ebitda_valuation(self,
                            ebitda: float,
                            industry_multiple: float,
                            net_debt: float) -> Dict[str, float]:
        """
        ارزش‌گذاری با روش EV/EBITDA
        
        Parameters:
        -----------
        ebitda: سود قبل از بهره، مالیات و استهلاک
        industry_multiple: ضریب صنعت
        net_debt: خالص بدهی (بدهی - وجه نقد)
        """
        
        try:
            enterprise_value = ebitda * industry_multiple
            equity_value = enterprise_value - net_debt
            
            return {
                'enterprise_value': enterprise_value,
                'equity_value': equity_value,
                'implied_multiple': industry_multiple,
                'ebitda': ebitda
            }
            
        except Exception as e:
            print(f"خطا در محاسبه EV/EBITDA: {e}")
            return {}
    
    def ps_valuation(self,
                     revenue: float,
                     industry_ps: float,
                     profit_margin_adjustment: float = 1.0) -> Dict[str, float]:
        """
        ارزش‌گذاری با روش P/S (قیمت به فروش)
        
        مفروضات:
        - مناسب برای شرکت‌های با سودآوری متغیر
        - P/S صنعت بر اساس میانه بازار
        - تعدیل بر اساس حاشیه سود
        
        Parameters:
        -----------
        revenue: درآمد (فروش) - میلیون ریال
        industry_ps: میانگین P/S صنعت
        profit_margin_adjustment: ضریب تعدیل حاشیه سود
        """
        
        try:
            adjusted_ps = industry_ps * profit_margin_adjustment
            equity_value = revenue * adjusted_ps
            
            return {
                'equity_value': equity_value,
                'implied_ps': adjusted_ps,
                'revenue': revenue,
                'assumptions': {
                    'industry_ps': industry_ps,
                    'margin_adjustment': profit_margin_adjustment
                }
            }
            
        except Exception as e:
            print(f"خطا در محاسبه P/S: {e}")
            return {}
    
    def residual_income_model(self,
                               book_value: float,
                               roe: float,
                               cost_of_equity: float,
                               projection_years: int = 5) -> Dict[str, float]:
        """
        مدل درآمد باقیمانده (Residual Income Model)
        
        مفروضات:
        - RI = NI - (BV × Re)
        - مناسب برای شرکت‌های با ارزش دفتری معتبر
        - فرض: بازده بالاتر از هزینه حقوق صاحبان سهام
        
        Parameters:
        -----------
        book_value: ارزش دفتری - میلیون ریال
        roe: بازده حقوق صاحبان سهام (%)
        cost_of_equity: هزینه حقوق صاحبان سهام (%)
        """
        
        try:
            # درآمد خالص
            net_income = book_value * roe
            
            # درآمد باقیمانده در هر سال
            pv_residual_income = 0
            current_bv = book_value
            
            for year in range(1, projection_years + 1):
                # درآمد خالص پیش‌بینی
                ni = current_bv * roe
                
                # هزینه سرمایه
                equity_charge = current_bv * cost_of_equity
                
                # درآمد باقیمانده
                ri = ni - equity_charge
                
                # تنزیل
                pv_ri = ri / ((1 + cost_of_equity) ** year)
                pv_residual_income += pv_ri
                
                # به‌روزرسانی ارزش دفتری
                current_bv = current_bv + ni - (ni * 0.3)  # فرض: 30% سود تقسیم می‌شود
            
            # ارزش پایانی RI
            terminal_ri = current_bv * (roe - cost_of_equity)
            pv_terminal_ri = terminal_ri / (cost_of_equity * ((1 + cost_of_equity) ** projection_years))
            
            # ارزش حقوق صاحبان سهام
            equity_value = book_value + pv_residual_income + pv_terminal_ri
            
            return {
                'equity_value': equity_value,
                'current_book_value': book_value,
                'pv_residual_income': pv_residual_income,
                'pv_terminal_ri': pv_terminal_ri,
                'roe': roe,
                'cost_of_equity': cost_of_equity,
                'explanation': f'ارزش = {book_value:,.0f} + {pv_residual_income:,.0f} + {pv_terminal_ri:,.0f}'
            }
            
        except Exception as e:
            print(f"خطا در محاسبه Residual Income: {e}")
            return {}
    
    def dividend_discount_model(self,
                                 current_dividend: float,
                                 growth_rate: float,
                                 required_return: float) -> Dict[str, float]:
        """
        مدل تنزیل سود نقدی (Gordon Growth Model)
        
        مفروضات:
        - مناسب برای شرکت‌های با سود نقدی منظم
        - فرض رشد ثابت سود
        - P = D₁ / (r - g)
        
        Parameters:
        -----------
        current_dividend: سود نقدی هر سهم سال جاری
        growth_rate: نرخ رشد سود (%)
        required_return: بازده مورد انتظار (%)
        """
        
        try:
            # سود سال بعد
            next_dividend = current_dividend * (1 + growth_rate)
            
            # ارزش سهم
            if required_return <= growth_rate:
                print(f"⚠️ بازده مورد انتظار باید بیشتر از نرخ رشد باشد")
                return {}
            
            value_per_share = next_dividend / (required_return - growth_rate)
            
            return {
                'value_per_share': value_per_share,
                'current_dividend': current_dividend,
                'next_dividend': next_dividend,
                'growth_rate': growth_rate,
                'required_return': required_return,
                'dividend_yield': current_dividend / value_per_share if value_per_share > 0 else 0
            }
            
        except Exception as e:
            print(f"خطا در محاسبه DDM: {e}")
            return {}
    
    def adjusted_present_value(self,
                                unlevered_fcf: float,
                                growth_rate: float,
                                unlevered_cost_of_equity: float,
                                debt_value: float,
                                interest_rate: float,
                                projection_years: int = 5) -> Dict[str, float]:
        """
        ارزش فعلی تعدیل شده (APV)
        
        مفروضات:
        - APV = NPV(Unlevered) + PV(Tax Shield)
        - مناسب برای شرکت‌های با ساختار سرمایه متغیر
        - نرخ مالیات: 25%
        
        Parameters:
        -----------
        unlevered_fcf: جریان نقدی بدون اهرم
        growth_rate: نرخ رشد
        unlevered_cost_of_equity: هزینه حقوق بدون اهرم
        debt_value: ارزش بدهی
        interest_rate: نرخ بهره
        """
        
        try:
            tax_rate = self.iran_assumptions['corporate_tax_rate']
            
            # 1. ارزش شرکت بدون اهرم
            pv_unlevered_fcf = 0
            for year in range(1, projection_years + 1):
                fcf = unlevered_fcf * ((1 + growth_rate) ** year)
                pv = fcf / ((1 + unlevered_cost_of_equity) ** year)
                pv_unlevered_fcf += pv
            
            # Terminal value
            terminal_fcf = unlevered_fcf * ((1 + growth_rate) ** projection_years) * (1 + growth_rate)
            terminal_value = terminal_fcf / (unlevered_cost_of_equity - growth_rate)
            pv_terminal = terminal_value / ((1 + unlevered_cost_of_equity) ** projection_years)
            
            unlevered_firm_value = pv_unlevered_fcf + pv_terminal
            
            # 2. ارزش فعلی سپر مالیاتی
            # Tax Shield = D × rd × T
            annual_tax_shield = debt_value * interest_rate * tax_rate
            pv_tax_shield = 0
            
            for year in range(1, projection_years + 1):
                pv_ts = annual_tax_shield / ((1 + interest_rate) ** year)
                pv_tax_shield += pv_ts
            
            # 3. APV
            firm_value = unlevered_firm_value + pv_tax_shield
            equity_value = firm_value - debt_value
            
            return {
                'firm_value': firm_value,
                'equity_value': equity_value,
                'unlevered_value': unlevered_firm_value,
                'pv_tax_shield': pv_tax_shield,
                'debt_value': debt_value,
                'explanation': f'APV = {unlevered_firm_value:,.0f} + {pv_tax_shield:,.0f} = {firm_value:,.0f}'
            }
            
        except Exception as e:
            print(f"خطا در محاسبه APV: {e}")
            return {}
    
    def comprehensive_valuation(self,
                                 scenario_params: Dict[str, any],
                                 scenario_name: str = "خنثی") -> Dict[str, any]:
        """
        ارزش‌گذاری جامع با تمام روش‌ها و مفروضات شفاف
        
        روش‌های ارزش‌گذاری:
        1. DCF (Discounted Cash Flow) - با تحلیل حساسیت
        2. P/E (Price to Earnings) - تعدیل شده برای رشد
        3. P/B (Price to Book) - مبتنی بر ROE
        4. EV/EBITDA - ضریب صنعت
        5. P/S (Price to Sales) - برای شرکت‌های کم‌سود
        6. RIM (Residual Income Model) - مبتنی بر ارزش دفتری
        7. DDM (Dividend Discount Model) - برای سودهای منظم
        8. APV (Adjusted Present Value) - با سپر مالیاتی
        
        Parameters:
        -----------
        scenario_params: پارامترهای سناریو شامل تمام ورودی‌های لازم
        scenario_name: نام سناریو (خوشبینانه، خنثی، بدبینانه)
        """
        
        print(f"\n{'='*70}")
        print(f"ارزش‌گذاری جامع {self.company_name} - سناریوی {scenario_name}")
        print(f"{'='*70}")
        print(f"\n📋 مفروضات کلیدی بازار ایران:")
        print(f"  • نرخ بهره بدون ریسک: {self.iran_assumptions['risk_free_rate']:.1%}")
        print(f"  • صرف ریسک بازار: {self.iran_assumptions['market_risk_premium']:.1%}")
        print(f"  • نرخ تورم: {self.iran_assumptions['inflation_rate']:.1%}")
        print(f"  • نرخ مالیات شرکتی: {self.iran_assumptions['corporate_tax_rate']:.1%}")
        print(f"{'='*70}")
        
        results = {
            'company': self.company_name,
            'scenario': scenario_name,
            'iran_assumptions': self.iran_assumptions,
            'dcf': {},
            'pe': {},
            'pb': {},
            'ev_ebitda': {},
            'ps': {},
            'rim': {},  # Residual Income Model
            'ddm': {},  # Dividend Discount Model
            'apv': {},  # Adjusted Present Value
            'wacc_calc': {}
        }
        
        # محاسبه WACC اگر اطلاعات موجود باشد
        if all(k in scenario_params for k in ['equity_value', 'debt_value', 'cost_of_equity', 'cost_of_debt']):
            results['wacc_calc'] = self.calculate_wacc(
                equity_value=scenario_params['equity_value'],
                debt_value=scenario_params['debt_value'],
                cost_of_equity=scenario_params['cost_of_equity'],
                cost_of_debt=scenario_params['cost_of_debt']
            )
            print(f"\n⚖️ WACC محاسبه شده: {results['wacc_calc'].get('wacc', 0):.2%}")
        
        # DCF Valuation - با تحلیل حساسیت
        if all(k in scenario_params for k in ['fcf', 'growth_rate', 'discount_rate', 'terminal_growth']):
            print(f"\n💵 DCF - جریان نقدی آزاد تنزیل شده")
            print(f"  مفروضات:")
            print(f"    • FCF پایه: {scenario_params['fcf']:,.0f} میلیون ریال")
            print(f"    • نرخ رشد: {scenario_params['growth_rate']:.1%}")
            print(f"    • نرخ تنزیل (WACC): {scenario_params['discount_rate']:.1%}")
            print(f"    • رشد پایدار: {scenario_params['terminal_growth']:.1%}")
            
            results['dcf'] = self.dcf_valuation(
                free_cash_flow=scenario_params['fcf'],
                growth_rate=scenario_params['growth_rate'],
                discount_rate=scenario_params['discount_rate'],
                terminal_growth=scenario_params['terminal_growth'],
                detailed=True
            )
            if results['dcf']:
                ev = results['dcf']['enterprise_value']
                tv_pct = results['dcf'].get('terminal_percent', 0)
                print(f"  نتیجه: {ev:,.0f} میلیون ریال")
                print(f"  (ارزش پایانی: {tv_pct:.1f}% از کل)")
        
        # P/E Valuation
        if all(k in scenario_params for k in ['earnings', 'industry_pe']):
            print(f"\n📊 P/E - قیمت به سود")
            print(f"  مفروضات:")
            print(f"    • سود خالص: {scenario_params['earnings']:,.0f} میلیون ریال")
            print(f"    • P/E صنعت: {scenario_params['industry_pe']:.1f}")
            
            results['pe'] = self.pe_valuation(
                earnings=scenario_params['earnings'],
                industry_pe=scenario_params['industry_pe']
            )
            if results['pe']:
                print(f"  نتیجه: {results['pe']['equity_value']:,.0f} میلیون ریال")
        
        # P/B Valuation
        if all(k in scenario_params for k in ['book_value', 'roe', 'required_return']):
            print(f"\n📚 P/B - قیمت به ارزش دفتری")
            print(f"  مفروضات:")
            print(f"    • ارزش دفتری: {scenario_params['book_value']:,.0f} میلیون ریال")
            print(f"    • ROE: {scenario_params['roe']:.1%}")
            print(f"    • بازده مورد انتظار: {scenario_params['required_return']:.1%}")
            
            results['pb'] = self.pb_valuation(
                book_value=scenario_params['book_value'],
                roe=scenario_params['roe'],
                required_return=scenario_params['required_return']
            )
            if results['pb']:
                print(f"  نتیجه: {results['pb']['equity_value']:,.0f} میلیون ریال")
        
        # EV/EBITDA Valuation
        if all(k in scenario_params for k in ['ebitda', 'industry_ebitda_multiple', 'net_debt']):
            print(f"\n🏭 EV/EBITDA - ارزش شرکت به سود عملیاتی")
            print(f"  مفروضات:")
            print(f"    • EBITDA: {scenario_params['ebitda']:,.0f} میلیون ریال")
            print(f"    • ضریب صنعت: {scenario_params['industry_ebitda_multiple']:.1f}x")
            
            results['ev_ebitda'] = self.ev_ebitda_valuation(
                ebitda=scenario_params['ebitda'],
                industry_multiple=scenario_params['industry_ebitda_multiple'],
                net_debt=scenario_params['net_debt']
            )
            if results['ev_ebitda']:
                print(f"  نتیجه: {results['ev_ebitda']['equity_value']:,.0f} میلیون ریال")
        
        # P/S Valuation
        if all(k in scenario_params for k in ['revenue', 'industry_ps']):
            print(f"\n💼 P/S - قیمت به فروش")
            print(f"  مفروضات:")
            print(f"    • فروش: {scenario_params['revenue']:,.0f} میلیون ریال")
            print(f"    • P/S صنعت: {scenario_params['industry_ps']:.2f}")
            
            results['ps'] = self.ps_valuation(
                revenue=scenario_params['revenue'],
                industry_ps=scenario_params['industry_ps']
            )
            if results['ps']:
                print(f"  نتیجه: {results['ps']['equity_value']:,.0f} میلیون ریال")
        
        # Residual Income Model
        if all(k in scenario_params for k in ['book_value', 'roe', 'cost_of_equity']):
            print(f"\n🔷 RIM - مدل درآمد باقیمانده")
            print(f"  مفروضات: ارزش افزوده اقتصادی (EVA)")
            
            results['rim'] = self.residual_income_model(
                book_value=scenario_params['book_value'],
                roe=scenario_params['roe'],
                cost_of_equity=scenario_params['cost_of_equity']
            )
            if results['rim']:
                print(f"  نتیجه: {results['rim']['equity_value']:,.0f} میلیون ریال")
        
        # Dividend Discount Model (اگر سود نقدی منظم دارد)
        if all(k in scenario_params for k in ['dividend_per_share', 'dividend_growth', 'required_return']):
            print(f"\n💰 DDM - مدل تنزیل سود نقدی (Gordon)")
            print(f"  مفروضات: سود نقدی منظم و رشد ثابت")
            
            results['ddm'] = self.dividend_discount_model(
                current_dividend=scenario_params['dividend_per_share'],
                growth_rate=scenario_params['dividend_growth'],
                required_return=scenario_params['required_return']
            )
            if results['ddm']:
                print(f"  نتیجه: {results['ddm']['value_per_share']:,.0f} ریال/سهم")
        
        # APV - برای شرکت‌های با اهرم بالا
        if all(k in scenario_params for k in ['unlevered_fcf', 'unlevered_cost_equity', 'debt_value', 'interest_rate']):
            print(f"\n⚡ APV - ارزش فعلی تعدیل شده")
            print(f"  مفروضات: سپر مالیاتی بدهی")
            
            results['apv'] = self.adjusted_present_value(
                unlevered_fcf=scenario_params['unlevered_fcf'],
                growth_rate=scenario_params.get('growth_rate', 0.10),
                unlevered_cost_of_equity=scenario_params['unlevered_cost_equity'],
                debt_value=scenario_params['debt_value'],
                interest_rate=scenario_params['interest_rate']
            )
            if results['apv']:
                print(f"  نتیجه: {results['apv']['equity_value']:,.0f} میلیون ریال")
        
        # جمع‌آوری نتایج و محاسبه آماره‌ها
        equity_values = []
        methods_used = []
        
        if results['dcf'] and 'enterprise_value' in results['dcf']:
            equity_values.append(results['dcf']['enterprise_value'])
            methods_used.append('DCF')
        if results['pe'] and 'equity_value' in results['pe']:
            equity_values.append(results['pe']['equity_value'])
            methods_used.append('P/E')
        if results['pb'] and 'equity_value' in results['pb']:
            equity_values.append(results['pb']['equity_value'])
            methods_used.append('P/B')
        if results['ev_ebitda'] and 'equity_value' in results['ev_ebitda']:
            equity_values.append(results['ev_ebitda']['equity_value'])
            methods_used.append('EV/EBITDA')
        if results['ps'] and 'equity_value' in results['ps']:
            equity_values.append(results['ps']['equity_value'])
            methods_used.append('P/S')
        if results['rim'] and 'equity_value' in results['rim']:
            equity_values.append(results['rim']['equity_value'])
            methods_used.append('RIM')
        if results['apv'] and 'equity_value' in results['apv']:
            equity_values.append(results['apv']['equity_value'])
            methods_used.append('APV')
        
        if equity_values:
            # آمارهای مرکزی
            results['average_valuation'] = np.mean(equity_values)
            results['median_valuation'] = np.median(equity_values)
            results['min_valuation'] = np.min(equity_values)
            results['max_valuation'] = np.max(equity_values)
            results['std_valuation'] = np.std(equity_values)
            
            # ضریب تغییرات (نشان‌دهنده پراکندگی)
            cv = results['std_valuation'] / results['average_valuation'] if results['average_valuation'] > 0 else 0
            results['coefficient_of_variation'] = cv
            
            # میانگین وزنی (وزن بیشتر به DCF و RIM)
            weights = {
                'DCF': 0.30,
                'RIM': 0.20,
                'P/E': 0.15,
                'P/B': 0.15,
                'EV/EBITDA': 0.10,
                'P/S': 0.05,
                'APV': 0.05
            }
            
            weighted_sum = 0
            total_weight = 0
            for method, value in zip(methods_used, equity_values):
                weight = weights.get(method, 0.10)
                weighted_sum += value * weight
                total_weight += weight
            
            results['weighted_average'] = weighted_sum / total_weight if total_weight > 0 else results['average_valuation']
            results['methods_used'] = methods_used
            results['values_list'] = equity_values
            
            # نمایش خلاصه
            print(f"\n{'='*70}")
            print(f"📊 خلاصه ارزش‌گذاری - سناریوی {scenario_name}")
            print(f"{'='*70}")
            print(f"روش‌های استفاده شده: {', '.join(methods_used)}")
            print(f"\n📈 آمارهای ارزش‌گذاری (میلیون ریال):")
            print(f"  • میانگین ساده: {results['average_valuation']:,.0f}")
            print(f"  • میانگین وزنی: {results['weighted_average']:,.0f} ⭐")
            print(f"  • میانه: {results['median_valuation']:,.0f}")
            print(f"  • حداقل: {results['min_valuation']:,.0f}")
            print(f"  • حداکثر: {results['max_valuation']:,.0f}")
            print(f"  • انحراف معیار: {results['std_valuation']:,.0f}")
            print(f"  • ضریب تغییرات: {cv:.1%} {'(پراکندگی بالا)' if cv > 0.25 else '(پراکندگی پایین)'}")
            print(f"{'='*70}")
        
        self.valuation_results[scenario_name] = results
        
        return results


if __name__ == "__main__":
    # تست ارزش‌گذار
    pass
