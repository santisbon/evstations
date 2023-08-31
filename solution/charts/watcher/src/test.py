import logging
import utils
import unittest

# DEBUG | INFO | WARNING | ERROR | CRITICAL
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

class TestWatcher(unittest.TestCase):
  def test_get_content(self):
    msg = r'{"id":"10852202","type":"mention","created_at":"2023-08-22T03:49:09.445Z","account":{"id":"110929884415845373","username":"santisbon","acct":"santisbon@mstdn.social","display_name":"","locked":true,"bot":false,"discoverable":false,"group":false,"created_at":"2022-11-29T00:00:00.000Z","note":"<p>Account used only for testing federation between Mastodon and Firefish servers.</p>","url":"https://mstdn.social/@santisbon","avatar":"https://botsin.space/avatars/original/missing.png","avatar_static":"https://botsin.space/avatars/original/missing.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":5,"last_status_at":"2023-08-21","emojis":[],"fields":[]},"status":{"id":"110931224121753495","created_at":"2023-08-22T03:49:02.000Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"direct","language":"en","uri":"https://mstdn.social/users/santisbon/statuses/110931223645261881","url":"https://mstdn.social/@santisbon/110931223645261881","replies_count":0,"reblogs_count":0,"favourites_count":0,"edited_at":null,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"content":"<p><span class=\"h-card\"><a href=\"https://botsin.space/@ev\" class=\"u-url mention\" rel=\"nofollow noopener noreferrer\" target=\"_blank\">@<span>ev</span></a></span> Golden Gate Bridge</p>","filtered":[],"reblog":null,"account":{"id":"110929884415845373","username":"santisbon","acct":"santisbon@mstdn.social","display_name":"","locked":true,"bot":false,"discoverable":false,"group":false,"created_at":"2022-11-29T00:00:00.000Z","note":"<p>Account used only for testing federation between Mastodon and Firefish servers.</p>","url":"https://mstdn.social/@santisbon","avatar":"https://botsin.space/avatars/original/missing.png","avatar_static":"https://botsin.space/avatars/original/missing.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":5,"last_status_at":"2023-08-21","emojis":[],"fields":[]},"media_attachments":[],"mentions":[{"id":"110926228642265467","username":"ev","url":"https://botsin.space/@ev","acct":"ev"}],"tags":[],"emojis":[],"card":null,"poll":null}}'
    self.assertEqual(utils.get_content(msg), 'Golden Gate Bridge')

  def test_get_content_truncated(self):
    msg = r'{"id":"10851535","type":"mention","created_at":"2023-08-22T02:41:57.944Z","account":{"id":"110894545590921511","username":"santisbon","acct":"santisbon@firefish.social","display_name":"Armando :verified_root:","locked":false,"bot":false,"discoverable":true,"group":false,"created_at":"2023-08-15T00:00:00.000Z","note":"<p><span>Solution architecture, cloud computing, software engineering, AI/ML, dogs, sports.</span></p>","url":"https://firefish.social/@santisbon","avatar":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","avatar_static":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":20,"last_status_at":"2023-08-15","emojis":[{"shortcode":"verified_root","url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/original/078a1e76a3fe761e.png","static_url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/static/078a1e76a3fe761e.png","visible_in_picker":true}],"fields":[{"name":"GitHub","value":"<a href=\"https://github.com/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">github.com/santisbon</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.239+00:00"},{"name":"Blog","value":"<a href=\"https://dev.to/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">dev.to/santisbon</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.282+00:00"},{"name":"Custom emojis","value":"<a href=\"https://emojos.santisbon.me/\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">emojos.santisbon.me/</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.624+00:00"}]},"status":{"id":"110930959915530812","created_at":"2023-08-22T02:41:56.969Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"direct","language":null,"uri":"https://firefish.social/notes/9ip9l5ntvsnkuiqi","url":"https://firefish.social/notes/9ip9l5ntvsnkuiqi","replies_count":0,"reblogs_count":0,"favourites_count":0,"edited_at":null,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"content":"<p><a href=\"https://botsin.space/@ev\" class=\"u-url mention\" rel=\"nofollow noopener noreferrer\" target=\"_blank\">@ev@botsin.space</a><span> Wrigley building</span></p>","filtered":[],"reblog":null,"account":{"id":"110894545590921511","username":"santisbon","acct":"santisbon@firefish.social","display_name":"Armando :verified_root:","locked":false,"bot":false,"discoverable":true,"group":false,"created_at":"2023-08-15T00:00:00.000Z","note":"<p><span>Solution architecture, cloud computing, software engineering, AI/ML, dogs, sports.</span></p>","url":"https://firefish.social/@santisbon","avatar":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","avatar_static":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":20,"last_status_at":"2023-08-15","emojis":[{"shortcode":"verified_root","url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/original/078a1e76a3fe761e.png","static_url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/static/078a1e76a3fe761e.png","visible_in_picker":true}],"fields":[{"name":"GitHub","value":"<a href=\"https://github.com/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span'
    self.assertEqual(utils.get_content(msg), 'Wrigley building')

  def test_get_status(self):
    msg = r'{"id":"10852202","type":"mention","created_at":"2023-08-22T03:49:09.445Z","account":{"id":"110929884415845373","username":"santisbon","acct":"santisbon@mstdn.social","display_name":"","locked":true,"bot":false,"discoverable":false,"group":false,"created_at":"2022-11-29T00:00:00.000Z","note":"<p>Account used only for testing federation between Mastodon and Firefish servers.</p>","url":"https://mstdn.social/@santisbon","avatar":"https://botsin.space/avatars/original/missing.png","avatar_static":"https://botsin.space/avatars/original/missing.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":5,"last_status_at":"2023-08-21","emojis":[],"fields":[]},"status":{"id":"110931224121753495","created_at":"2023-08-22T03:49:02.000Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"direct","language":"en","uri":"https://mstdn.social/users/santisbon/statuses/110931223645261881","url":"https://mstdn.social/@santisbon/110931223645261881","replies_count":0,"reblogs_count":0,"favourites_count":0,"edited_at":null,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"content":"<p><span class=\"h-card\"><a href=\"https://botsin.space/@ev\" class=\"u-url mention\" rel=\"nofollow noopener noreferrer\" target=\"_blank\">@<span>ev</span></a></span> Golden Gate Bridge</p>","filtered":[],"reblog":null,"account":{"id":"110929884415845373","username":"santisbon","acct":"santisbon@mstdn.social","display_name":"","locked":true,"bot":false,"discoverable":false,"group":false,"created_at":"2022-11-29T00:00:00.000Z","note":"<p>Account used only for testing federation between Mastodon and Firefish servers.</p>","url":"https://mstdn.social/@santisbon","avatar":"https://botsin.space/avatars/original/missing.png","avatar_static":"https://botsin.space/avatars/original/missing.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":5,"last_status_at":"2023-08-21","emojis":[],"fields":[]},"media_attachments":[],"mentions":[{"id":"110926228642265467","username":"ev","url":"https://botsin.space/@ev","acct":"ev"}],"tags":[],"emojis":[],"card":null,"poll":null}}'
    self.assertEqual(utils.get_status_id(msg), '110931224121753495')

  def test_get_status_truncated(self):
    msg = r'{"id":"10851535","type":"mention","created_at":"2023-08-22T02:41:57.944Z","account":{"id":"110894545590921511","username":"santisbon","acct":"santisbon@firefish.social","display_name":"Armando :verified_root:","locked":false,"bot":false,"discoverable":true,"group":false,"created_at":"2023-08-15T00:00:00.000Z","note":"<p><span>Solution architecture, cloud computing, software engineering, AI/ML, dogs, sports.</span></p>","url":"https://firefish.social/@santisbon","avatar":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","avatar_static":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":20,"last_status_at":"2023-08-15","emojis":[{"shortcode":"verified_root","url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/original/078a1e76a3fe761e.png","static_url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/static/078a1e76a3fe761e.png","visible_in_picker":true}],"fields":[{"name":"GitHub","value":"<a href=\"https://github.com/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">github.com/santisbon</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.239+00:00"},{"name":"Blog","value":"<a href=\"https://dev.to/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">dev.to/santisbon</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.282+00:00"},{"name":"Custom emojis","value":"<a href=\"https://emojos.santisbon.me/\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">emojos.santisbon.me/</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.624+00:00"}]},"status":{"id":"110930959915530812","created_at":"2023-08-22T02:41:56.969Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"direct","language":null,"uri":"https://firefish.social/notes/9ip9l5ntvsnkuiqi","url":"https://firefish.social/notes/9ip9l5ntvsnkuiqi","replies_count":0,"reblogs_count":0,"favourites_count":0,"edited_at":null,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"content":"<p><a href=\"https://botsin.space/@ev\" class=\"u-url mention\" rel=\"nofollow noopener noreferrer\" target=\"_blank\">@ev@botsin.space</a><span> Wrigley building</span></p>","filtered":[],"reblog":null,"account":{"id":"110894545590921511","username":"santisbon","acct":"santisbon@firefish.social","display_name":"Armando :verified_root:","locked":false,"bot":false,"discoverable":true,"group":false,"created_at":"2023-08-15T00:00:00.000Z","note":"<p><span>Solution architecture, cloud computing, software engineering, AI/ML, dogs, sports.</span></p>","url":"https://firefish.social/@santisbon","avatar":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","avatar_static":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":20,"last_status_at":"2023-08-15","emojis":[{"shortcode":"verified_root","url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/original/078a1e76a3fe761e.png","static_url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/static/078a1e76a3fe761e.png","visible_in_picker":true}],"fields":[{"name":"GitHub","value":"<a href=\"https://github.com/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span'
    self.assertEqual(utils.get_status_id(msg), '110930959915530812')

  def test_get_account(self):
    msg = r'{"id":"10852202","type":"mention","created_at":"2023-08-22T03:49:09.445Z","account":{"id":"110929884415845373","username":"santisbon","acct":"santisbon@mstdn.social","display_name":"","locked":true,"bot":false,"discoverable":false,"group":false,"created_at":"2022-11-29T00:00:00.000Z","note":"<p>Account used only for testing federation between Mastodon and Firefish servers.</p>","url":"https://mstdn.social/@santisbon","avatar":"https://botsin.space/avatars/original/missing.png","avatar_static":"https://botsin.space/avatars/original/missing.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":5,"last_status_at":"2023-08-21","emojis":[],"fields":[]},"status":{"id":"110931224121753495","created_at":"2023-08-22T03:49:02.000Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"direct","language":"en","uri":"https://mstdn.social/users/santisbon/statuses/110931223645261881","url":"https://mstdn.social/@santisbon/110931223645261881","replies_count":0,"reblogs_count":0,"favourites_count":0,"edited_at":null,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"content":"<p><span class=\"h-card\"><a href=\"https://botsin.space/@ev\" class=\"u-url mention\" rel=\"nofollow noopener noreferrer\" target=\"_blank\">@<span>ev</span></a></span> Golden Gate Bridge</p>","filtered":[],"reblog":null,"account":{"id":"110929884415845373","username":"santisbon","acct":"santisbon@mstdn.social","display_name":"","locked":true,"bot":false,"discoverable":false,"group":false,"created_at":"2022-11-29T00:00:00.000Z","note":"<p>Account used only for testing federation between Mastodon and Firefish servers.</p>","url":"https://mstdn.social/@santisbon","avatar":"https://botsin.space/avatars/original/missing.png","avatar_static":"https://botsin.space/avatars/original/missing.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":5,"last_status_at":"2023-08-21","emojis":[],"fields":[]},"media_attachments":[],"mentions":[{"id":"110926228642265467","username":"ev","url":"https://botsin.space/@ev","acct":"ev"}],"tags":[],"emojis":[],"card":null,"poll":null}}'
    self.assertEqual(utils.get_account(msg), '@santisbon@mstdn.social')
  
  def test_get_account_truncated(self):
    msg = r'{"id":"10851535","type":"mention","created_at":"2023-08-22T02:41:57.944Z","account":{"id":"110894545590921511","username":"santisbon","acct":"santisbon@firefish.social","display_name":"Armando :verified_root:","locked":false,"bot":false,"discoverable":true,"group":false,"created_at":"2023-08-15T00:00:00.000Z","note":"<p><span>Solution architecture, cloud computing, software engineering, AI/ML, dogs, sports.</span></p>","url":"https://firefish.social/@santisbon","avatar":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","avatar_static":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":20,"last_status_at":"2023-08-15","emojis":[{"shortcode":"verified_root","url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/original/078a1e76a3fe761e.png","static_url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/static/078a1e76a3fe761e.png","visible_in_picker":true}],"fields":[{"name":"GitHub","value":"<a href=\"https://github.com/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">github.com/santisbon</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.239+00:00"},{"name":"Blog","value":"<a href=\"https://dev.to/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">dev.to/santisbon</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.282+00:00"},{"name":"Custom emojis","value":"<a href=\"https://emojos.santisbon.me/\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span><span class=\"\">emojos.santisbon.me/</span><span class=\"invisible\"></span></a>","verified_at":"2023-08-15T16:21:28.624+00:00"}]},"status":{"id":"110930959915530812","created_at":"2023-08-22T02:41:56.969Z","in_reply_to_id":null,"in_reply_to_account_id":null,"sensitive":false,"spoiler_text":"","visibility":"direct","language":null,"uri":"https://firefish.social/notes/9ip9l5ntvsnkuiqi","url":"https://firefish.social/notes/9ip9l5ntvsnkuiqi","replies_count":0,"reblogs_count":0,"favourites_count":0,"edited_at":null,"favourited":false,"reblogged":false,"muted":false,"bookmarked":false,"content":"<p><a href=\"https://botsin.space/@ev\" class=\"u-url mention\" rel=\"nofollow noopener noreferrer\" target=\"_blank\">@ev@botsin.space</a><span> Wrigley building</span></p>","filtered":[],"reblog":null,"account":{"id":"110894545590921511","username":"santisbon","acct":"santisbon@firefish.social","display_name":"Armando :verified_root:","locked":false,"bot":false,"discoverable":true,"group":false,"created_at":"2023-08-15T00:00:00.000Z","note":"<p><span>Solution architecture, cloud computing, software engineering, AI/ML, dogs, sports.</span></p>","url":"https://firefish.social/@santisbon","avatar":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","avatar_static":"https://files.botsin.space/cache/accounts/avatars/110/894/545/590/921/511/original/5a82dc0e6c67a979.png","header":"https://botsin.space/headers/original/missing.png","header_static":"https://botsin.space/headers/original/missing.png","followers_count":0,"following_count":2,"statuses_count":20,"last_status_at":"2023-08-15","emojis":[{"shortcode":"verified_root","url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/original/078a1e76a3fe761e.png","static_url":"https://files.botsin.space/cache/custom_emojis/images/000/292/460/static/078a1e76a3fe761e.png","visible_in_picker":true}],"fields":[{"name":"GitHub","value":"<a href=\"https://github.com/santisbon\" target=\"_blank\" rel=\"nofollow noopener noreferrer\"><span class=\"invisible\">https://</span'
    self.assertEqual(utils.get_account(msg), '@santisbon@firefish.social')

suite = unittest.TestLoader().loadTestsFromTestCase(TestWatcher)
unittest.TextTestRunner(verbosity=2).run(suite)
