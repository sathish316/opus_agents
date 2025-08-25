"""
Mock Agent System - Simulates PydanticAI functionality for demonstration.
This shows how the agent system would work without requiring PydanticAI dependency.
"""

from pydantic import BaseModel
from typing import Type, TypeVar, Any

T = TypeVar('T', bound=BaseModel)


class MockAgent:
    """Mock agent that simulates PydanticAI Agent functionality."""
    
    def __init__(self, model: str, result_type: Type[T], system_prompt: str):
        self.model = model
        self.result_type = result_type
        self.system_prompt = system_prompt
    
    def run_sync(self, user_input: str) -> 'MockResult':
        """
        Mock run_sync that generates responses based on the analysis context.
        In a real implementation, this would call the LLM.
        """
        # Parse the analysis context to generate appropriate responses
        response_text = self._generate_mock_response(user_input)
        
        # Create the result object
        try:
            result_data = self._parse_response_to_model(response_text)
            return MockResult(data=result_data)
        except Exception as e:
            # Fallback to basic response
            return MockResult(data=self._create_fallback_response())
    
    def _generate_mock_response(self, context: str) -> str:
        """Generate a mock response based on the analysis context."""
        if "Equity Portfolio Analysis" in context:
            return self._generate_equity_response(context)
        elif "Debt Portfolio Analysis" in context:
            return self._generate_debt_response(context)
        elif "Hybrid Portfolio Analysis" in context:
            return self._generate_hybrid_response(context)
        elif "Gold/Silver Portfolio Analysis" in context:
            return self._generate_gold_silver_response(context)
        elif "Portfolio Allocation Analysis" in context:
            return self._generate_ratio_response(context)
        elif "Comprehensive Portfolio Analysis" in context:
            return self._generate_comprehensive_response(context)
        else:
            return "Analysis completed successfully."
    
    def _generate_equity_response(self, context: str) -> str:
        """Generate equity-specific recommendation."""
        if "Performance gap: -" in context:
            return ("Your equity portfolio is underperforming the benchmark. Consider switching to "
                   "low-cost index funds like UTI Nifty Index Fund or SBI Sensex Index Fund for "
                   "better long-term returns. These funds have lower expense ratios and track "
                   "market indices closely.")
        else:
            return ("Your equity portfolio is performing well. Continue your SIP investments "
                   "and maintain diversification across large-cap index funds.")
    
    def _generate_debt_response(self, context: str) -> str:
        """Generate debt-specific recommendation."""
        if "Performance gap: -" in context:
            return ("Your debt portfolio returns are below expectations. Consider moving to "
                   "higher-yielding debt funds like SBI Magnum Gilt Fund or HDFC Short Term "
                   "Debt Fund. Also ensure adequate liquidity with liquid funds.")
        else:
            return ("Your debt portfolio provides stable returns. Maintain allocation for "
                   "capital preservation and portfolio stability.")
    
    def _generate_hybrid_response(self, context: str) -> str:
        """Generate hybrid-specific recommendation."""
        if "Performance gap: -" in context:
            return ("Your hybrid funds are underperforming. Consider switching to balanced "
                   "advantage funds like HDFC Balanced Advantage Fund or ICICI Balanced "
                   "Advantage Fund which dynamically adjust equity-debt allocation.")
        else:
            return ("Your hybrid funds provide good balanced exposure. Continue investments "
                   "for moderate risk-adjusted returns.")
    
    def _generate_gold_silver_response(self, context: str) -> str:
        """Generate gold/silver-specific recommendation."""
        if "Gold allocation:" in context and "Silver allocation:" in context:
            return ("Maintain a 50:50 gold-silver allocation for optimal portfolio hedging. "
                   "Consider Nippon India Gold Savings Fund and Kotak Silver ETF Fund for "
                   "exposure to precious metals as inflation hedge.")
        else:
            return ("Add precious metals exposure (5% of portfolio) for diversification and "
                   "inflation protection through gold and silver funds.")
    
    def _generate_ratio_response(self, context: str) -> str:
        """Generate asset allocation recommendation."""
        if "Rebalancing Required: True" in context:
            return ("Your portfolio allocation deviates from optimal targets. Rebalance by "
                   "adjusting SIP amounts or switching investments to align with your age "
                   "and risk profile. Focus on systematic rebalancing quarterly.")
        else:
            return ("Your asset allocation is well-balanced for your age and risk profile. "
                   "Continue current investment strategy with periodic reviews.")
    
    def _generate_comprehensive_response(self, context: str) -> str:
        """Generate comprehensive portfolio recommendation."""
        risk_score = 0
        if "Risk Score:" in context:
            try:
                risk_line = [line for line in context.split('\n') if 'Risk Score:' in line][0]
                risk_score = int(risk_line.split('Risk Score: ')[1].split('/')[0])
            except:
                risk_score = 50
        
        if risk_score > 60:
            return ("HIGH PRIORITY: Your portfolio requires immediate attention. Multiple fund "
                   "categories are underperforming and allocation is suboptimal. Focus on: "
                   "1) Switch underperforming funds to marquee index funds, "
                   "2) Rebalance asset allocation, "
                   "3) Increase SIP amounts in better-performing categories.")
        elif risk_score > 30:
            return ("MODERATE PRIORITY: Your portfolio has some areas for improvement. "
                   "Consider gradual rebalancing and switching 1-2 underperforming funds "
                   "to better alternatives. Maintain your SIP discipline.")
        else:
            return ("GOOD: Your portfolio is well-structured and performing adequately. "
                   "Continue current investment strategy with annual reviews and minor "
                   "adjustments as needed.")
    
    def _parse_response_to_model(self, response: str) -> BaseModel:
        """Parse response text into the expected result model."""
        # This is a simplified parser - in reality, you'd use proper LLM response parsing
        if hasattr(self.result_type, '__annotations__'):
            kwargs = {}
            annotations = self.result_type.__annotations__
            
            if 'recommendation' in annotations:
                kwargs['recommendation'] = response
            if 'overall_recommendation' in annotations:
                kwargs['overall_recommendation'] = response
                
            return self.result_type(**kwargs)
        
        return self.result_type()
    
    def _create_fallback_response(self) -> BaseModel:
        """Create a fallback response when parsing fails."""
        if hasattr(self.result_type, '__annotations__'):
            kwargs = {}
            annotations = self.result_type.__annotations__
            
            for field_name, field_type in annotations.items():
                if field_name == 'recommendation':
                    kwargs[field_name] = "Analysis completed. Please review your portfolio performance."
                elif field_name == 'overall_recommendation':
                    kwargs[field_name] = "Portfolio analysis completed successfully."
                elif field_name == 'funds_analyzed':
                    kwargs[field_name] = 0
                elif field_name == 'total_invested':
                    kwargs[field_name] = 0.0
                elif field_name == 'current_value':
                    kwargs[field_name] = 0.0
                elif field_name == 'portfolio_xirr':
                    kwargs[field_name] = 0.0
                elif field_name == 'benchmark_xirr':
                    kwargs[field_name] = 0.0
                elif field_name == 'recommended_funds':
                    kwargs[field_name] = []
                elif field_name == 'action_required':
                    kwargs[field_name] = False
                elif field_name == 'gold_allocation':
                    kwargs[field_name] = 0.0
                elif field_name == 'silver_allocation':
                    kwargs[field_name] = 0.0
                elif field_name == 'age_group':
                    kwargs[field_name] = "30-40"
                elif field_name == 'risk_profile':
                    kwargs[field_name] = "MODERATE"
                elif field_name == 'current_allocation':
                    # Import here to avoid circular imports
                    from agents.ratio_analyzer import OptimalAllocation
                    kwargs[field_name] = OptimalAllocation(equity_ratio=0.0, debt_ratio=0.0, hybrid_ratio=0.0, gold_silver_ratio=0.0)
                elif field_name == 'optimal_allocation':
                    from agents.ratio_analyzer import OptimalAllocation
                    kwargs[field_name] = OptimalAllocation(equity_ratio=0.0, debt_ratio=0.0, hybrid_ratio=0.0, gold_silver_ratio=0.0)
                elif field_name == 'allocation_gap':
                    from agents.ratio_analyzer import OptimalAllocation
                    kwargs[field_name] = OptimalAllocation(equity_ratio=0.0, debt_ratio=0.0, hybrid_ratio=0.0, gold_silver_ratio=0.0)
                elif field_name == 'rebalancing_required':
                    kwargs[field_name] = False
                elif field_name == 'risk_score':
                    kwargs[field_name] = 0.0
                elif field_name == 'action_items':
                    kwargs[field_name] = []
                elif field_name == 'equity_analysis':
                    kwargs[field_name] = "No analysis available"
                elif field_name == 'debt_analysis':
                    kwargs[field_name] = "No analysis available"
                elif field_name == 'hybrid_analysis':
                    kwargs[field_name] = "No analysis available"
                elif field_name == 'gold_silver_analysis':
                    kwargs[field_name] = "No analysis available"
                elif field_name == 'allocation_analysis':
                    kwargs[field_name] = "No analysis available"
                elif 'str' in str(field_type):
                    kwargs[field_name] = "Default"
                elif 'int' in str(field_type):
                    kwargs[field_name] = 0
                elif 'float' in str(field_type):
                    kwargs[field_name] = 0.0
                elif 'bool' in str(field_type):
                    kwargs[field_name] = False
                elif 'list' in str(field_type) or 'List' in str(field_type):
                    kwargs[field_name] = []
                    
            return self.result_type(**kwargs)
        
        return self.result_type()


class MockResult:
    """Mock result that simulates PydanticAI RunResult."""
    
    def __init__(self, data: BaseModel):
        self.data = data


# Export the mock agent as the main Agent class
Agent = MockAgent