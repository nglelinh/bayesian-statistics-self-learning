require 'digest'

module Jekyll
  class AccessGateGenerator < Generator
    safe true
    priority :highest

    def generate(site)
      config = site.config['access_gate'] || {}
      enabled = config['enabled'] == true
      password = config['password'].to_s

      payload = {
        'enabled' => false,
        'password_hash' => nil,
        'session_key' => normalized_session_key(config['session_key'])
      }

      unless enabled
        site.config['access_gate_payload'] = payload
        return
      end

      if password.empty?
        Jekyll.logger.warn('AccessGate:', 'access_gate.enabled is true but access_gate.password is blank. The gate will stay disabled.')
        site.config['access_gate_payload'] = payload
        return
      end

      payload['enabled'] = true
      payload['password_hash'] = Digest::SHA256.hexdigest(password)
      site.config['access_gate_payload'] = payload
    end

    private

    def normalized_session_key(raw_value)
      key = raw_value.to_s.strip
      return 'bayesian-statistics-self-learning-access' if key.empty?

      key
    end
  end
end
