from charms.docker.compose import Compose
from charms.docker import compose
from mock import patch
import pytest

class TestCompose:

    # This has limited usefulness, it fails when used with the @patch
    # decorator. simply pass in compose to any object to gain the
    # test fixture
    @pytest.fixture
    def compose(self):
        return Compose('files/test', strict=False)

    def test_init_strict(self):
        with patch('charms.docker.compose.Workspace.validate') as f:
            c = Compose('test', strict=True)
            # Is this the beast? is mock() doing the right thing here?
            f.assert_called_with()

    def test_init_workspace(self, compose):
        assert "{}".format(compose.workspace) == "files/test"

    def test_start_service(self, compose):
        with patch('charms.docker.compose.Compose.run') as s:
            compose.up('nginx')
            expect = 'docker-compose up -d nginx'
            s.assert_called_with(expect)

    def test_start_default_formation(self, compose):
        with patch('charms.docker.compose.Compose.run') as s:
            compose.up()
            expect = 'docker-compose up -d'
            s.assert_called_with(expect)

    def test_kill_service(self, compose):
        with patch('charms.docker.compose.Compose.run') as s:
            compose.kill('nginx')
            expect = 'docker-compose kill nginx'
            s.assert_called_with(expect)

    def test_kill_service_default(self, compose):
        with patch('charms.docker.compose.Compose.run') as s:
            compose.kill()
            expect = 'docker-compose kill'
            s.assert_called_with(expect)

    def test_rm_service_default(self, compose):
        with patch('charms.docker.compose.Compose.run') as s:
            compose.rm()
            expect = 'docker-compose rm'
            s.assert_called_with(expect)

    def test_rm_service(self, compose):
        with patch('charms.docker.compose.Compose.run') as s:
            compose.rm('nginx')
            expect = 'docker-compose rm nginx'
            s.assert_called_with(expect)

    @patch('charms.docker.compose.chdir')
    @patch('charms.docker.compose.check_output')
    def test_run(self, ccmock, chmock):
        compose = Compose('files/workspace', strict=False)
        compose.up('nginx')
        chmock.assert_called_with('files/workspace')
        ccmock.assert_called_with(['docker-compose', 'up', '-d', 'nginx'])

    # This test is a little ugly but is a byproduct of testing the callstack.
    @patch('os.getcwd')
    def test_context_manager(self, cwdmock):
        cwdmock.return_value = '/tmp'
        with patch('os.chdir') as chmock:
            compose = Compose('files/workspace', strict=False)
            with patch('charms.docker.compose.check_output'):
                compose.up('nginx')
                # We can only test the return called with in this manner.
                # So check that we at least reset context
                chmock.assert_called_with('/tmp')
                # TODO: test that we've actually tried to change dir context
