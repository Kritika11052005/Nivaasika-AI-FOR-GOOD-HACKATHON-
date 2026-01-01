from utils.database import execute_query

def calculate_risk_score(findings):
    """
    Calculate risk score based on findings
    Uses weighted scoring: severity × defect weight
    """
    defect_weights = {
        'structural': 3.0,  # Most critical
        'wiring': 2.5,
        'leak': 2.0,
        'damp': 1.8,
        'crack': 1.5,
        'finishing': 1.0    # Least critical
    }
    
    total_score = 0
    for finding in findings:
        defect_type = finding.get('defect_type', 'finishing')
        severity = finding.get('severity', 1)
        weight = defect_weights.get(defect_type, 1.0)
        
        total_score += severity * weight
    
    return round(total_score, 2)

def assign_risk_level(risk_score):
    """
    Assign risk level based on score
    """
    if risk_score <= 20:
        return 'Low'
    elif risk_score <= 50:
        return 'Medium'
    else:
        return 'High'

def calculate_renovation_costs(findings):
    """
    Calculate total renovation cost range based on defects
    Returns: (min_cost, max_cost)
    """
    # Get improvement rules from database
    rules_result = execute_query("SELECT * FROM IMPROVEMENT_RULES")
    
    if not rules_result or not rules_result.get('data'):
        return (0, 0)
    
    # Create rules lookup
    rules = {}
    for row in rules_result['data']:
        rule_id, defect_type, sev_min, sev_max, action, cost_range, priority = row
        
        if defect_type not in rules:
            rules[defect_type] = []
        
        rules[defect_type].append({
            'severity_min': sev_min,
            'severity_max': sev_max,
            'cost_range': cost_range,
            'action': action,
            'priority': priority
        })
    
    # Calculate costs
    total_min = 0
    total_max = 0
    
    for finding in findings:
        defect_type = finding.get('defect_type')
        severity = finding.get('severity', 1)
        
        if defect_type in rules:
            # Find matching rule
            for rule in rules[defect_type]:
                if rule['severity_min'] <= severity <= rule['severity_max']:
                    # Parse cost range (e.g., "Rs 5,000 - Rs 20,000")
                    cost_range = rule['cost_range']
                    min_cost, max_cost = parse_cost_range(cost_range)
                    total_min += min_cost
                    total_max += max_cost
                    break
    
    return (total_min, total_max)

def parse_cost_range(cost_str):
    """
    Parse cost range string like "Rs 5,000 - Rs 20,000" or "Rs 2,00,000+"
    Returns: (min_cost, max_cost)
    """
    try:
        # Remove "Rs" and spaces
        cost_str = cost_str.replace('Rs', '').replace(' ', '')
        
        if '+' in cost_str:
            # Handle "2,00,000+" format
            min_cost = int(cost_str.replace('+', '').replace(',', ''))
            max_cost = min_cost * 2  # Estimate max as 2x min
        elif '-' in cost_str:
            # Handle "5,000-20,000" format
            parts = cost_str.split('-')
            min_cost = int(parts[0].replace(',', ''))
            max_cost = int(parts[1].replace(',', ''))
        else:
            # Single value
            min_cost = int(cost_str.replace(',', ''))
            max_cost = min_cost
        
        return (min_cost, max_cost)
    except:
        return (0, 0)

def get_improvement_recommendations(findings):
    """
    Generate improvement recommendations based on findings
    Returns: List of recommendations with priorities
    """
    # Get improvement rules
    rules_result = execute_query("SELECT * FROM IMPROVEMENT_RULES")
    
    if not rules_result or not rules_result.get('data'):
        return []
    
    # Create rules lookup
    rules = {}
    for row in rules_result['data']:
        rule_id, defect_type, sev_min, sev_max, action, cost_range, priority = row
        
        if defect_type not in rules:
            rules[defect_type] = []
        
        rules[defect_type].append({
            'severity_min': sev_min,
            'severity_max': sev_max,
            'cost_range': cost_range,
            'action': action,
            'priority': priority
        })
    
    recommendations = []
    
    # Group findings by defect type
    defect_groups = {}
    for finding in findings:
        defect_type = finding.get('defect_type')
        if defect_type not in defect_groups:
            defect_groups[defect_type] = []
        defect_groups[defect_type].append(finding)
    
    # Generate recommendations
    for defect_type, defect_findings in defect_groups.items():
        if defect_type in rules:
            # Get max severity for this defect type
            max_severity = max([f.get('severity', 1) for f in defect_findings])
            
            # Find matching rule
            for rule in rules[defect_type]:
                if rule['severity_min'] <= max_severity <= rule['severity_max']:
                    # Get affected rooms
                    affected_rooms = list(set([f.get('room_name') for f in defect_findings]))
                    
                    recommendations.append({
                        'defect_type': defect_type,
                        'action': rule['action'],
                        'cost_range': rule['cost_range'],
                        'priority': rule['priority'],
                        'affected_rooms': ', '.join(affected_rooms),
                        'count': len(defect_findings)
                    })
                    break
    
    # Sort by priority
    priority_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 5))
    
    return recommendations

def get_statistics(findings):
    """
    Calculate statistics from findings
    """
    total_defects = len(findings)
    critical_issues = len([f for f in findings if f.get('severity', 0) >= 8])
    affected_rooms = len(set([f.get('room_name') for f in findings]))
    
    # Count by defect type
    defect_counts = {}
    for finding in findings:
        defect_type = finding.get('defect_type', 'unknown')
        defect_counts[defect_type] = defect_counts.get(defect_type, 0) + 1
    
    return {
        'total_defects': total_defects,
        'critical_issues': critical_issues,
        'affected_rooms': affected_rooms,
        'defect_counts': defect_counts
    }