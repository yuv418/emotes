class ApiKey < ApplicationRecord
  belongs_to :user
  attr_reader :jwt
  has_secure_password :key

  before_validation on: :create do
    tmp_key = SecureRandom.base64 48
    self.key = tmp_key.deep_dup
    @payload = { key: tmp_key } # So we can encode the unhashed key
  end

  after_save do
    @payload[:id] = id
    @jwt = JWT.encode(@payload, Rails.application.secret_key_base)
  end

end
