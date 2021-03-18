class EmoteType < ActiveRecord::Base
  enum emote_type: [:gif, :png]
end
